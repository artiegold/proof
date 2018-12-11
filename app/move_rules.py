import db_interface

class IllegalRequestException(Exception):
    """General exception for illegal requests to this module."""
    pass


class move_rules:
    def __init__(self, db, get_image):
        self.db = db
        self.get_image = get_image

    def move_rule_after(self, rule_id, target):
            """Move a rule after a given rule."""
            def find_place(target, rules):
                i = 0
                while i < len(rules):
                    if rules[i].id == target:
                        if i == len(rules) - 1:
                            return rules[i], None, i
                        return rules[i], rules[i + 1], i
                    i += 1
                return None, None, -1

            if rule_id == target:
                raise IllegalRequestException('rule and target are the same')
            rules = self.db.get_rules()
            this, next, index = find_place(target, rules)
            if this is None:
                return False # the target was not found
            if next is None:
                new_priority = this.priority + 100
            elif next.id == rule_id:
                return True # it is already there

            if next.priority - this.priority > 1:
                new_priority = (this.priority + next.priority) // 2
            else:
                self.db.rules_rewrite_priorities(rules, rule_id, index, self.db.AFTER)

            self.db.rule_change_priority(rule_id, new_priority)
            self.get_image.update_rules(self.db.get_rules())
            return True 

    def move_rule_before(self, rule_id, target):
        """Move a rule before a given rule."""
        def find_place(target, rules):
            i = 0
            prev = None
            while i < len(rules):
                if rules[i].id == target:
                    return prev, rules[i], i
                i += 1
                prev = rules[i]
            return None, None, -1

        if rule_id == target:
            raise IllegalRequestException('rule and target are the same')
        rules = self.db.get_rules()
        prev, this, index = find_place(target, rules)
    
        if this is None:
            return False # the target was not found
        
        if prev is None:
            new_priority = this.priority // 2
        else:
            if prev.id == rule_id:
                return True # it is already there

            if this.priority - prev.priority > 1:
                new_priority = (prev.priority + this.priority) // 2
            else:
                self.db.rules_rewrite_priorities(rules, rule_id, index, self.db.BEFORE)
                return True

        self.db.rule_change_priority(rule_id, new_priority)
        self.get_image.update_rules(self.db.get_rules())
        return True 
