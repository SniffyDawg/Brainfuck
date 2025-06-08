#!/usr/bin/env python3
"""
Brainfuck Interpreter

Brainfuck is an esoteric programming language with only 8 commands:
> : Move the pointer to the right
< : Move the pointer to the left
+ : Increment the memory cell under the pointer
- : Decrement the memory cell under the pointer
. : Output the character signified by the cell at the pointer
, : Input a character and store it in the cell at the pointer
[ : Jump past the matching ] if the cell under the pointer is 0
] : Jump back to the matching [ if the cell under the pointer is nonzero
"""

import sys
from typing import List, Optional


class BrainfuckInterpreter:
    def __init__(self, memory_size: int = 30000):
        """
        Initialize the Brainfuck interpreter.
        
        Args:
            memory_size: Size of the memory array (default: 30000)
        """
        self.memory: List[int] = [0] * memory_size
        self.pointer: int = 0
        self.instruction_pointer: int = 0
        self.output: List[str] = []
        self.input_buffer: str = ""
        self.input_index: int = 0
        
    def set_input(self, input_string: str):
        """
        Set the input string for the program.
        
        Args:
            input_string: String to use as input for ',' commands
        """
        self.input_buffer = input_string
        self.input_index = 0
        
    def find_matching_bracket(self, code: str, start_pos: int, direction: int) -> Optional[int]:
        """
        Find the matching bracket for loop constructs.
        
        Args:
            code: The Brainfuck code
            start_pos: Starting position to search from
            direction: 1 for forward (find ]), -1 for backward (find [)
            
        Returns:
            Position of matching bracket or None if not found
        """
        bracket_count = 1  # Start with 1 since we're looking for the matching bracket
        pos = start_pos
        open_bracket = '[' if direction == 1 else ']'
        close_bracket = ']' if direction == 1 else '['
        
        while 0 <= pos < len(code):
            if code[pos] == open_bracket:
                bracket_count += 1
            elif code[pos] == close_bracket:
                bracket_count -= 1
                if bracket_count == 0:
                    return pos
            pos += direction
            
        return None
        
    def execute(self, code: str, input_string: str = "") -> str:
        """
        Execute a Brainfuck program.
        
        Args:
            code: The Brainfuck code to execute
            input_string: Input string for the program
            
        Returns:
            Output string produced by the program
        """
        # Reset interpreter state
        self.memory = [0] * len(self.memory)
        self.pointer = 0
        self.instruction_pointer = 0
        self.output = []
        self.set_input(input_string)
        
        # Filter out non-command characters
        valid_commands = set('><+-.,[]')
        filtered_code = ''.join(c for c in code if c in valid_commands)
        
        while self.instruction_pointer < len(filtered_code):
            command = filtered_code[self.instruction_pointer]
            
            if command == '>':
                # Move pointer right
                self.pointer += 1
                if self.pointer >= len(self.memory):
                    raise RuntimeError("Memory pointer out of bounds (too high)")
                    
            elif command == '<':
                # Move pointer left
                self.pointer -= 1
                if self.pointer < 0:
                    raise RuntimeError("Memory pointer out of bounds (too low)")
                    
            elif command == '+':
                # Increment memory cell
                self.memory[self.pointer] = (self.memory[self.pointer] + 1) % 256
                
            elif command == '-':
                # Decrement memory cell
                self.memory[self.pointer] = (self.memory[self.pointer] - 1) % 256
                
            elif command == '.':
                # Output character
                self.output.append(chr(self.memory[self.pointer]))
                
            elif command == ',':
                # Input character
                if self.input_index < len(self.input_buffer):
                    self.memory[self.pointer] = ord(self.input_buffer[self.input_index])
                    self.input_index += 1
                else:
                    # No more input available, set to 0
                    self.memory[self.pointer] = 0
                    
            elif command == '[':
                # Jump forward if current cell is 0
                if self.memory[self.pointer] == 0:
                    matching_bracket = self.find_matching_bracket(
                        filtered_code, self.instruction_pointer + 1, 1
                    )
                    if matching_bracket is None:
                        raise RuntimeError("Unmatched '[' bracket")
                    self.instruction_pointer = matching_bracket
                    
            elif command == ']':
                # Jump backward if current cell is not 0
                if self.memory[self.pointer] != 0:
                    matching_bracket = self.find_matching_bracket(
                        filtered_code, self.instruction_pointer - 1, -1
                    )
                    if matching_bracket is None:
                        raise RuntimeError(f"Unmatched ']' bracket at position {self.instruction_pointer}")
                    self.instruction_pointer = matching_bracket
                    
            self.instruction_pointer += 1
            
        return ''.join(self.output)


def main():
    """
    Main function to run the Brainfuck interpreter from command line.
    """
    if len(sys.argv) < 2:
        print("Usage: python brainfuck_interpreter.py <brainfuck_file> [input_string]")
        print("\nExample Brainfuck programs:")
        print("Hello World: ++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.")
        print("Cat program: ,[.,]")
        return
        
    filename = sys.argv[1]
    input_string = sys.argv[2] if len(sys.argv) > 2 else ""
    
    try:
        with open(filename, 'r') as file:
            code = file.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return
    except Exception as e:
        print(f"Error reading file: {e}")
        return
        
    interpreter = BrainfuckInterpreter()
    
    try:
        output = interpreter.execute(code, input_string)
        print(output, end='')  # Don't add extra newline
    except Exception as e:
        print(f"Runtime error: {e}")


if __name__ == "__main__":
    main()

