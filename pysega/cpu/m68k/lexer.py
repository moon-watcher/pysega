from pysega.base.lexer import Lexer as BaseLexer

class Lexer(BaseLexer):

    ''' Motorola 68000 Conditions Set '''
    ASM_CONDITIONS = [
        'CC', 'CS', 'EQ', 'GE', 'GT', 'HI',
        'LE', 'LS', 'LT', 'MI', 'NE', 'PL',
        'VC', 'VS'
    ]

    ''' Motorola 68000 Instructions Set '''
    ASM_INSTRUCTIONS = [
        'ABCD', 'ADD', 'ADDA', 'ADDI', 'ADDQ', 'ADDX',
        'AND', 'ANDI', 'ASL', 'ASR', 'Bcc', 'BCHG',
        'BCLR', 'BRA', 'BSET', 'BSR', 'BTST', 'CHK', 'CLR', 'CMP',
        'CMPA', 'CMPI', 'CMPM', 'DBcc', 'DBF', 'DIVS', 'DIVU',
        'EOR', 'EORI', 'EXG', 'EXT', 'ILLEGAL', 'JMP',
        'JSR', 'LEA', 'LINK', 'LSL', 'LSR', 'MOVE', 'MOVEA',
        'MOVEP', 'MOVEQ', 'MULS', 'MULU', 'NBCD', 'NEG', 'NEGX',
        'NOP', 'NOT', 'OR', 'ORI', 'PEA', 'RESET', 'ROL', 'ROR',
        'ROXL', 'ROXR', 'RTE', 'RTR', 'RTS', 'SBCD', 'Scc',
        'STOP', 'SUB', 'SUBA', 'SUBI', 'SUBQ', 'SUBX', 'SWAP',
        'TAS', 'TRAP', 'TRAPV', 'TST', 'UNLK',
    ]

    ''' Motorola 68000 Registers Set '''
    ASM_REGISTERS = [
        'D0', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7',
        'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7',
        'PC', 'SR', 'CCR'
    ]

    ''' Motorola 68000 Sizes Set '''
    ASM_SIZES = [
        'BYTE', 'WORD', 'LONG'
    ]

    ''' Motorola 68000 Types Set '''
    ASM_TYPES = [
        'BINARY', 'DECIMAL', 'OCTAL', 'HEXADECIMAL',
        'STRING',
        'OFFSET'
    ]

    """ LEX Tokens """
    tokens = BaseLexer.tokens \
        + ['INSTRUCTION', 'SIZE', 'REGISTER'] \
        + ASM_TYPES

    """ Return Opcodes List """
    def getInstructions(self):
        temp = []
        for instruction in self.ASM_INSTRUCTIONS:
            if "cc" not in instruction:
                temp.append(instruction)
            else:
                for condition in self.ASM_CONDITIONS:
                    temp.append(instruction.replace('cc', condition))
        return temp

    """ LEX Tokens Function Rules """
    def t_ID(self, t):
        r"[0-9A-Za-z_:]+"
        instructions = self.getInstructions()
        if t.value.upper() in instructions:
            t.type = 'INSTRUCTION'
            t.value = t.value.upper()
        elif t.value.upper() in self.ASM_REGISTERS:
            t.type = 'REGISTER'
            t.value = t.value.upper()
        return t

    def t_SIZE(self, t):
        r"(?:\.)[b|w|l|s|B|W|L|S]"
        if t.value.upper() == '.L':
            t.value = 'LONG'
        elif t.value.upper() == '.W':
            t.value = 'WORD'
        elif t.value.upper() == '.B':
            t.value = 'BYTE'
        return t

    def t_STRING(self, t):
        r"((?:[\"])(.*?)(?:[\"])|(?:[\'])(.*?)(?:[\']))"
        t.value = t.value[1:-1]
        return t

    def t_BINARY(self, t):
        r"(?:\#\%)[0-1]+"
        t.value = int(t.value[2:],2)
        return t

    def t_DECIMAL(self, t):
        r"(?:\#)[0-9]+"
        t.value = int(t.value[1:],10)
        return t

    def t_OCTAL(self, t):
        r"(?:\#\@)[0-7]+"
        t.value = int(t.value[2:],8)
        return t

    def t_HEXADECIMAL(self, t):
        r"(?:\#\$)([0-9A-Fa-f]+)"
        t.value = int(t.value[2:],16)
        return t

    def t_OFFSET(self, t):
        r"(?:\$)[0-9A-Fa-f]+"
        t.value = int(t.value[1:],16)
        return t
