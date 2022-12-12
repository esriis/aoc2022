from __future__ import annotations

class Monkey():
    def __init__(
        self,
        number: int,
        items: list[int],
        divisible_by: int,
        monkey_true: int,
        monkey_false: int,
        op_add: int = 0,
        op_mult: int = 1,
        op_power: int = 1,
        inspections: int = 0
    ):
        self.number = number
        self.items = items
        self.divisible_by = divisible_by
        self.monkey_true = monkey_true
        self.monkey_false = monkey_false
        self.op_add = op_add
        self.op_mult = op_mult
        self.op_power = op_power
        self.inspections = inspections
    
    def catch(self, item: int):
        self.items.append(item)
    
    def take_turn(self, monkey_dict: dict[Monkey], worry_mode: str = "normal", denominator: int = 1):
        while len(self.items) > 0:
            item = self.items.pop(0)
            if worry_mode == "normal":
                item = self._inspect_item(item) 
                item = item // 3
            elif worry_mode == "stressed":
                item = item % denominator
                item = self._inspect_item(item) 
            divisible = self._test_item(item)
            monkey = monkey_dict[self.monkey_true] if divisible else monkey_dict[self.monkey_false]
            self._throw(item=item, monkey=monkey)
        
    def _inspect_item(self, item: int) -> int:
        item = self.op_mult*item**self.op_power + self.op_add
        self.inspections += 1
        return item

    def _test_item(self, item: int) -> bool:
        return item % self.divisible_by == 0

    def _throw(self, item: int, monkey: Monkey):
        monkey.catch(item=item)
            
    
    @classmethod
    def parse_monkey(cls, monkey_str: str):
        lines = monkey_str.split("\n")
        number = int(lines[0][-2])
        items = [int(item) for item in lines[1][18:].split(", ")]
        divisible_by = int(lines[3][21:])
        monkey_true = int(lines[4][-1])
        monkey_false = int(lines[5][-1])
        if lines[2][23] == "*":
            if lines[2][25:28] == "old":
                op_mult = 1
                op_add = 0
                op_power = 2
            else:
                op_mult = int(lines[2][25:])
                op_add = 0
                op_power = 1
        elif lines[2][23] == "+":
            op_add = int(lines[2][25:])
            op_mult = 1
            op_power = 1
        return cls(
            number=number,
            items = items,
            divisible_by = divisible_by,
            monkey_true=monkey_true,
            monkey_false=monkey_false,
            op_add=op_add,
            op_mult=op_mult,
            op_power=op_power
        )