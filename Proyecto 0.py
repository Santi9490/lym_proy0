import re

TOKENS = [
    (r'defVar', 'DEFVAR'),
    (r'defProc', 'DEFPROC'),
    (r'jump|walk|leap|turn|turnto|drop|get|grap|letGo|nop', 'INSTRUCTIONS'),
    (r'if|else|while|repeat|times', 'CONDITIONAL'),
    (r'either|front|right|left|back|around', 'DIRECTION'),
    (r'north|south|west|east', 'FACING'),
    (r'can', 'CAN'),
    (r'not', 'NOT'),
    (r'\)|\(', 'PAREN'),
    (r'\{|\}', 'BRACE'),
    (r',', 'COMMA'),
    (r';', 'SEMICOLON'),
    (r'[a-zA-Z_]\w*', 'IDENTIFIER'),
    (r'\d+', 'NUMBER'),
    (r'=', 'EQUALS'),
]

dicc_defVar={ }
list_intruction=['jump','walk','leap','turn','turnto','drop','grap','letGo','nop']
list_conditional=['if','else','while','repeat','times']


def tokenize(program):
    tokens = []
    pattern = '|'.join(f'(?P<{name}>{regex})' for regex, name in TOKENS)
    for match in re.finditer(pattern, program, re.IGNORECASE):
        token_type = match.lastgroup
        token_value = match.group()
        tokens.append((token_type, token_value.lower()))
    return tokens


def validate_program(tokens):
    i = 0
    result=True
    while i < len(tokens):
        token_type, token_value = tokens[i]
        if token_type == 'DEFVAR':
            if i + 1 < len(tokens):
                next_token = tokens[i + 1]
                next_token_type, next_value = next_token
                if next_token_type != 'IDENTIFIER':
                    return False
                else:
                    if i + 2 < len(tokens):
                        value = tokens[i + 2]
                        value_type, value_value = value
                        if value_type not in ['NUMBER', 'IDENTIFIER']:
                            return False
                        else:
                            i+=2
                            dicc_defVar[next_value]= value_value
                            
                    else:
                        return False
            else:
                return False
        elif token_type == 'IDENTIFIER':
            result, val= parse_identifier(tokens, i)
            if not result:
                return False
            else:
                i=val
        elif token_type == 'DEFPROC':
            result, i = parse_deproc(tokens, i)
            if not result:
                return False
        elif token_type== 'INSTRUCTIONS':
            result, i = parse_instructions(tokens, i)
            if not result:
                return False
        elif token_type == 'CONDITIONAL':
            result, i = parse_conditionals(tokens, i)
            if not result:
                return False
        elif token_type == '{':
            i+=1
            result, i= ver_deproc(tokens, i)
        elif token_type == '}':
            return False
            

        i+=1
        
    return result

def ver_deproc(lista, pos):
    variable= lista[pos]
    variable_type, variable_value= variable
    
    if variable_type == 'INSTRUCTIONS':
        result , pos =parse_instructions(lista, pos)
        if not result:
            return False, pos
        
    elif variable_type == 'CONDITIONAL':
        result, pos = parse_conditionals(lista, pos)
        if not result:
            return False, pos
        
    elif variable_type== 'IDENTIFIER':
        result, pos= parse_identifier(lista, pos)
        if not result:
            return False, pos
    elif variable_type == 'DEFPROC':
        result, pos= parse_identifier(lista, pos)
        if not result:
            return False, pos
        
    elif variable_value =="}":
        return True, pos
    
    elif variable_value ==";":
        return ver_deproc (lista, pos+1)
    else:
        return False, pos
    
    return ver_deproc (lista, pos+1)
    
def parse_deproc(lista, pos):
    if pos+1< len(lista):
        pos+=1
        next_token= lista[pos]
        next_token_type, next_value = next_token
        if next_token_type!=  'IDENTIFIER':
            return False, pos
        else:
            result, pos= parse_identifier(lista, pos )
            if not result:
                return False, pos         
            else:
                if pos+1 < len(lista):
                    pos+=1
                    abrir = lista[pos]
                    abrir_type, abrir_value= abrir
                    if abrir_value != '{':
                        return False, pos
                    else:
                        if pos+1<len(lista):
                            pos+=1
                            result, pos = ver_deproc(lista, pos)
                            if not result:
                                return False, pos
                            else:
                                return True, pos
                                
                        else:
                            return False, pos
                        
                else: 
                    return False, pos
                            
                                
    else:
        return False, pos
    
def parse_identifier(lista, pos):   
    token= lista[pos]
    token_type, token_value= token
    before_token = lista[pos-1]
    before_type, before_value = before_token
    if before_type == 'DEFVAR':
        if pos + 1 < len(lista):
            value = lista[pos+1]
            value_type, value_value = value
            if value_type not in ['NUMBER', 'IDENTIFIER']:
                return False, pos
            else:
              dicc_defVar[token_value]=value_type
        else:
            return False, pos
        
    elif before_type == 'DEFPROC':
        if pos + 1 < len(lista):
            value = lista[pos+1]
            value_type, value_value = value
            pos+=1
            if value_type not in ['PAREN']:
                return False, pos
            else:
                if pos + 1 < len(lista):
                    pos+=1
                    siguiente= lista[pos]
                    siguiente_type, siguiente_value = siguiente
                    if siguiente_type in ['NUMBER', 'IDENTIFIER']:
                        if pos + 1 < len(lista):
                            if pos + 1 < len(lista):
                                pos+=1
                                coma= lista[pos]
                                coma_type, coma_value = coma
                                if coma_type not in ['COMMA', 'PAREN']:  
                                    return False, pos
                                else:
                                    if coma_type not in ['PAREN']:
                                        if pos + 1 < len(lista):
                                            pos+=1
                                            val2= lista[pos]
                                            val2_type, val2_value = val2
                                            if val2_type not in ['NUMBER', 'IDENTIFIER']:  
                                                return False, pos
                                            else: 
                                                if pos + 1 < len(lista):
                                                    pos+=1
                                                    siguiente2= lista[pos]
                                                    siguiente2_type, siguiente2_value = siguiente2
                                                    if siguiente2_type not in ['PAREN']:
                                                        return False, pos
                                                    else: 
                                                        dicc_defVar[token_value]= siguiente_value, val2_value
                                                        dicc_defVar[siguiente_value]=0
                                                        dicc_defVar[val2_value]=0
                                                else:
                                                    return False, pos
                                                
                                        else:
                                            return False, pos
                                    else:
                                        dicc_defVar[token_value]= val1_value
                            else:
                                return False, pos
                    else:
                        if siguiente_type not in ['PAREN']:
                            return False, pos
                        else:
                            dicc_defVar[token_value]= 0
                else:
                    return False, pos
        else:
            return False, pos
                                      
    else:
        if token not in dicc_defVar.keys() or dicc_defVar.values():      
            if pos + 1 < len(lista):
                pos+=1
                value = lista[pos]
                value_type, value_value = value
                if value_type not in ['PAREN']:
                    if pos + 1 < len(lista):
                        pos+=1
                        siguiente= lista[pos]
                        siguiente_type, siguiente_value = siguiente
                        if siguiente_type not in ['EQUALS']:
                            return False, pos
                        else:
                            if pos + 1 < len(lista):
                                pos+=1
                                val1=lista[pos]
                                val1_type, val1_value = val1
                                if val1_type not in ['NUMBER', 'IDENTIFIER']:
                                    return False, pos
                                else:
                                    if pos+1<len(lista):
                                        pos+=1
                                        pun_co=lista[pos]
                                        pun_co_type,pun_co_value=pun_co
                                        if pun_co_type not in  ['SEMICOLON']:
                                            return False, pos
                                        else:
                                            dicc_defVar[token_value]= val1_value
                                    else: 
                                        return False, pos
                                
                
                                
                            else: 
                                return False, pos
                            
                    else:
                        return False, pos
                    
                else:
                    if pos + 1 < len(lista):
                        pos+=1
                        val1=lista[pos]
                        val1_type, val1_value = val1
                        if  val1_type not in ['NUMBER', 'IDENTIFIER']:
                            if val1_type not in ['PAREN']:
                                return False, pos
                            else:
                                dicc_defVar[token_value] = 0
                        else:
                            
                            if pos + 1 < len(lista):
                                pos+=1
                                siguiente2= lista[pos]
                                siguiente2_type, siguiente2_value = siguiente2
                                if siguiente2_type not in ['COMMA', 'PAREN']:  
                                    return False, pos
                                else:
                                    if siguiente2_type not in ['COMMA']: 
                                        dicc_defVar[token_value] = val1_value
                                    else:
                                        if pos + 1 < len(lista):
                                            pos+=1
                                            val2=lista[pos]
                                            val2_type, val2_value = val2
                                            if  val2_type not in ['NUMBER', 'IDENTIFIER']:
                                                return False, pos
                                            else:
                                                if pos + 1 < len(lista):
                                                    pos+=1
                                                    siguiente2= lista[pos]
                                                    siguiente2_type, siguiente2_value = siguiente2
                                                    if siguiente2_type not in ['PAREN']:  
                                                        return False, pos
                                                    else: 
                                                        dicc_defVar[token_value]=val1, val2
                                                        
                                                else:
                                                    return False, pos
                                        else:
                                            return False, pos
                            else:
                                return False, pos
            else:
                return False, pos
        else: 
            return False, pos
    return True,pos

def parse_instructions(lista, pos):
    token= lista[pos]
    token_type, token_value= token
    
    if token_value == 'jump':
        result, pos=parse_jump(lista, pos)
        if not result:
            return False, pos
    elif token_value == 'walk' or token_value == 'leap':
        result, pos = parse_walk_or_leap(lista, pos)
        if not result:
            return False, pos
    elif token_value == 'drop' or token_value == 'get' or token_value == 'grap' or token_value == 'letgo':
        pos+=1
        result, pos= ver_one_paren(lista, pos)
        if not result:
            return False, pos
    elif token_value == 'nop': 
        pos+=1  
        parent= lista[pos]
        paren_type, paren_value= parent
        if paren_type not in ['PAREN']:
            return False, pos            
        else:
            if pos+1 < len(lista):
                pos+=1
                paren2= lista[pos]
                paren2_type, paren2_value=paren2
                if paren2_type not in ['PAREN']:
                    return False, pos
                
            else:
                return False, pos 
            
    elif token_value == 'turn':  
        parent= lista[pos]
        paren_type, paren_value= parent
        if paren_type not in ['PAREN']:
            return False, pos            
        else:
            if pos+1 < len(lista):
                pos+=1
                num1= lista[pos]
                num1_type, num1_value=num1
                if num1_type not in ['DIRECTION']:
                    return False, pos
                else:
                    if pos+1 <len(lista):
                        pos+=1
                        parent2 = lista[pos]
                        paren2_type, parent2_value= parent2
                        if paren_type not in ['PAREN']:
                            return False, pos
    
    elif token_value == 'turnto':  
        parent= lista[pos]
        paren_type, paren_value= parent
        if paren_type not in ['PAREN']:
            return False, pos            
        else:
            if pos+1 < len(lista):
                pos+=1
                num1= lista[pos]
                num1_type, num1_value=num1
                if num1_type not in ['FACING']:
                    return False, pos
                else:
                    if pos+1 <len(lista):
                        pos+=1
                        parent2 = lista[pos]
                        paren2_type, parent2_value= parent2
                        if paren_type not in ['PAREN']:
                            return False, pos
            else:
                return False, pos
        
    
    return True, pos
    
def parse_jump(lista, pos):
    if pos+1 <len(lista):
        pos+=1
        result, pos = ver_two_paren_val(lista, pos)
        if not result:
            return False, pos
        
        else:
            if pos+1 < len(lista): 
                pos+=1     
                semicolon= lista[pos]
                semicolon_type, semicolon_value=semicolon
                if semicolon_type in ['SEMICOLON']:
                    return True, pos
            else:
                return False, pos

    
    else:
        return False, pos
    
def parse_walk_or_leap(lista, pos):
    pos+=1
    result, num = ver_one_paren(lista, pos)
    if not result:
        result, num = ver_two_paren_O(lista, pos)
        if not result:
            result, num = ver_two_paren_D(lista, pos)
            if not result:
                return False, pos
            else:
                pos = num
                return True, pos
        else:
            pos = num
            return True, pos       
    else:
        pos = num
        return True, pos

def parse_conditionals(lista, pos):
    token= lista[pos]
    token_type, token_value= token
    if token_value == 'while':
        result, pos = parce_while(lista, pos)
        if not result:
            return False, pos
        else: 
            return True, pos
        
    elif token_value == 'if':
        result, pos = parce_if(lista, pos)
        if not result:
            return False, pos
        else: 
            return True, pos
        
    elif token_value == 'repeat':
        result, pos = parce_repeat(lista, pos)
        
    else:
        return False, pos
    
def parce_while(lista, pos):
    if pos +1 < len(lista):
        pos+=1
        can= lista[pos]
        can_type, can_value= can
        if can_type != 'CAN':
            return False, pos
        else:
            result, pos= parse_can(lista, pos)
            if not result:
                return False, pos
            else:
                if pos+1 <len(lista):
                    pos+=1
                    brace= lista[pos]
                    brace_type, brace_value= brace
                    if brace_value!="{":
                        return False, pos
                    else:
                        if pos + 1 < len(lista):
                            pos+=1
                            valor= lista[pos]
                            valor_type, valor_value= valor
                            if valor_type == 'INSTRUCTIONS':
                                result, pos = parse_instructions(lista, pos)
                                if not result:
                                    return False, pos
                                else:
                                    if pos+ 1< len(lista):
                                        pos+=1
                                        brace2= lista[pos]
                                        brace2_type, brace2_value= brace2
                                        if brace2_value!="}":
                                            return False, pos
                                        
                                    else:
                                        return False, pos
                            
                            elif valor_value != '}':
                                return False, pos
                        else:
                            return False, pos
                        
    
    else:
        return False, pos 
    
    return True, pos

def parce_if(lista, pos):
    if pos +1 < len(lista):
        pos+=1
        can= lista[pos]
        can_type, can_value= can
        if can_type != 'CAN':
            return False, pos
        else:
            result, pos= parse_can(lista, pos)
            if not result:
                return False, pos
            else:
                if pos+1 <len(lista):
                    pos+=1
                    brace= lista[pos]
                    brace_type, brace_value= brace
                    if brace_value!="{":
                        return False, pos
                    else:
                        if pos +1< len(lista):
                            pos+=1
                            result, pos = ver_deproc(lista, pos)
                            if not result:
                                return False, pos
                            else:                               
                                if pos+1 < len(lista):
                                    num_ver = pos +1
                                    hay_else= lista[num_ver]
                                    hay_else_type, hay_else_value= hay_else
                                    if hay_else_value == 'else':
                                        pos = num_ver
                                        if pos+1 < len(lista):
                                            pos+=1
                                            brace2= lista[pos]
                                            brace2_type, brace2_value= brace2
                                            if brace2_value!="{":
                                                return False, pos
                                            else:
                                                if pos +1< len(lista):
                                                    pos+=1
                                                    result, pos = ver_deproc(lista, pos)
                                                    if not result:
                                                        return False, pos
                                            
                                        else:
                                            return False, pos
                                            
                                    
                                    
                                else:
                                    return False, pos
                                
    return True, pos
            
def parce_repeat(lista, pos):
    if pos+1<len(lista):
        pos+=1
        num = lista[pos]
        num_type, num_value= num
        if num_type != 'NUMBER':
            return False, pos
        else: 
            if pos+1<len(lista):
                pos+=1
                times = lista[pos]
                times_type, times_value= num
                if times_value != 'times':
                    return False, pos
                else:
                    if pos+1 <len(lista):
                        pos+=1
                        brace= lista[pos]
                        brace_type, brace_value= brace
                        if brace_value!="{":
                            return False, pos
                        else:
                            if pos +1< len(lista):
                                pos+=1
                                result, pos = ver_deproc(lista, pos)
                                if not result:
                                    return False, pos
                                else:
                                    if pos +1 < len(lista):
                                        pos+=1
                                        brace= lista[pos]
                                        brace_type, brace_value= brace
                                        if brace_value!='}':
                                            return False, pos
                    
    else:
        return False, pos
    
    return True, pos                
    
def parse_can(lista, pos):
    pos+=1
    parent= lista[pos]
    parent_type, parent_value= parent
    if parent_value!= '(':
        return False, pos
    else:
        if pos + 1 < len(lista):
            pos+=1
            instruc= lista[pos]
            instruc_type, instruc_value= instruc
            if instruc_value in list_intruction:
                result, pos = parse_instructions(lista, pos)
                if not result:
                    return False, pos
                else:
                    if pos+1 < len(lista):
                        pos+=1
                        parent2= lista[pos]
                        parent2_type, parent2_value= parent2
                        if parent2_value == ')':
                            return True, pos
                        else: 
                            return False, pos
                    else:
                        return False, pos            
            else:
                return False, pos
    
    
def ver_one_paren(lista, pos):
    parent= lista[pos]
    paren_type, paren_value= parent
    if paren_type not in ['PAREN']:
        return False, pos            
    else:
        if pos+1 < len(lista):
            pos+=1
            num1= lista[pos]
            num1_type, num1_value=num1
            if num1_type not in ['NUMBER', 'IDENTIFIER']:
                return False, pos
            elif num1_type== 'IDENTIFIER' and ((num1_value in dicc_defVar.keys()) or (num1_value in dicc_defVar.values())):
                if pos+1 <len(lista):
                    pos+=1
                    parent2 = lista[pos]
                    paren2_type, parent2_value= parent2
                    if paren2_type not in ['PAREN']:
                        return False, pos
            elif num1_type== 'NUMBER':
                if pos+1 <len(lista):
                    pos+=1
                    parent2 = lista[pos]
                    paren2_type, parent2_value= parent2
                    if paren2_type not in ['PAREN']:
                        return False, pos
            else:
                return False, pos
                    
    return True, pos
                
   
def ver_two_paren_val(lista, pos):
    parent= lista[pos]
    paren_type, paren_value= parent
    if paren_type not in ['PAREN']:
        return False, pos            
    else:
        if pos+1 < len(lista):
            pos+=1
            num1= lista[pos]
            num1_type, num1_value=num1
            if num1_type not in ['NUMBER', 'IDENTIFIER']:
                return False, pos
            elif num1_type== 'IDENTIFIER' and (num1_value in dicc_defVar.keys() or num1_value in dicc_defVar.values()):
                if pos+1 < len(lista):
                    pos+=1
                    coma=lista[pos]
                    coma_type, coma_value= coma
                    if coma_type not in ['COMMA']:
                        return False, pos
                    else:
                        if pos+1 < len(lista):
                            pos+=1
                            num2=lista[pos]
                            num2_type, num2_value= num2
                            if num2_type not in ['NUMBER', 'IDENTIFIER']:
                                return False, pos
                            elif num2_type== 'IDENTIFIER' and (num2_value in dicc_defVar.keys or num2_value in dicc_defVar.values):
                                if pos+1 <len(lista):
                                    pos+=1
                                    parent2 = lista[pos]
                                    paren2_type, parent2_value= parent2
                                    if paren2_type not in ['PAREN']:
                                        return False, pos 
                            elif num2_type ==  'NUMBER':
                                if pos+1 <len(lista):
                                    pos+=1
                                    parent2 = lista[pos]
                                    paren2_type, parent2_value= parent2
                                    if paren2_type not in ['PAREN']:
                                        return False, pos
                            else: 
                                return False, pos
                                                                 
                        else: 
                            return False, pos
                else:
                    return False, pos
            elif num1_type == 'NUMBER':
                if pos+1 < len(lista):
                    pos+=1
                    coma=lista[pos]
                    coma_type, coma_value= coma
                    if coma_type not in ['COMMA']:
                        return False, pos
                    else:
                        if pos+1 < len(lista):
                            pos+=1
                            num2=lista[pos]
                            num2_type, num2_value= num2
                            if num2_type not in ['NUMBER', 'IDENTIFIER']:
                                return False, pos
                            elif num2_type== 'IDENTIFIER' and (num2_value in dicc_defVar.keys or num2_value in dicc_defVar.values):
                                if pos+1 <len(lista):
                                    pos+=1
                                    parent2 = lista[pos]
                                    paren2_type, parent2_value= parent2
                                    if paren2_type not in ['PAREN']:
                                        return False, pos 
                            elif num2_type ==  'NUMBER':
                                if pos+1 <len(lista):
                                    pos+=1
                                    parent2 = lista[pos]
                                    paren2_type, parent2_value= parent2
                                    if paren2_type not in ['PAREN']:
                                        return False, pos
                            else: 
                                return False, pos
                                                                 
                        else: 
                            return False, pos
                else:
                    return False, pos
            else:
                return False, pos
                
        else: 
            return False, pos
    
    return True, pos
    
def ver_two_paren_O(lista, pos): 
    parent= lista[pos]
    paren_type, paren_value= parent
    if paren_type not in ['PAREN']:
        return False, pos            
    else:
        if pos+1 < len(lista):
            pos+=1
            num1= lista[pos]
            num1_type, num1_value=num1
            if num1_type not in ['NUMBER', 'IDENTIFIER']:
                return False, pos
            elif num1_type== 'IDENTIFIER' and (num1_value in dicc_defVar.keys() or num1_value in dicc_defVar.values()):
                if pos+1 < len(lista):
                    pos+=1
                    coma=lista[pos]
                    coma_type, coma_value= coma
                    if coma_type not in ['COMMA']:
                        return False, pos
                    else:
                        if pos+1 < len(lista):
                            pos+=1
                            num2=lista[pos]
                            num2_type, num2_value= num2
                            if num2_type not in ['FACING']:
                                return False, pos
                            else:
                                if pos+1 <len(lista):
                                    pos+=1
                                    parent2 = lista[pos]
                                    paren2_type, parent2_value= parent2
                                    if paren2_type not in ['PAREN']:
                                        return False, pos  
                                else:
                                    return False, pos
                                                                  
                        else: 
                            return False, pos
                else:
                    return False, pos
            elif num1_type == 'NUMBER':
                if pos+1 < len(lista):
                    pos+=1
                    coma=lista[pos]
                    coma_type, coma_value= coma
                    if coma_type not in ['COMMA']:
                        return False, pos
                    else:
                        if pos+1 < len(lista):
                            pos+=1
                            num2=lista[pos]
                            num2_type, num2_value= num2
                            if num2_type not in ['FACING']:
                                return False, pos
                            else:
                                if pos+1 <len(lista):
                                    pos+=1
                                    parent2 = lista[pos]
                                    paren2_type, parent2_value= parent2
                                    if paren2_type not in ['PAREN']:
                                        return False, pos  
                                else:
                                    return False, pos
                                                                  
                        else: 
                            return False, pos
                else:
                    return False, pos
            else:
                return False, pos
                
        else: 
            return False, pos
    
    return True, pos   

def ver_two_paren_D(lista, pos):
    parent= lista[pos]
    paren_type, paren_value= parent
    if paren_type not in ['PAREN']:
        return False, pos            
    else:
        if pos+1 < len(lista):
            pos+=1
            num1= lista[pos]
            num1_type, num1_value=num1
            if num1_type not in ['NUMBER', 'IDENTIFIER']:
                return False, pos
            elif num1_type== 'IDENTIFIER' and (num1_value in dicc_defVar.keys() or num1_value in dicc_defVar.values()):
                if pos+1 < len(lista):
                    pos+=1
                    coma=lista[pos]
                    coma_type, coma_value= coma
                    if coma_type not in ['COMMA']:
                        return False, pos
                    else:
                        if pos+1 < len(lista):
                            pos+=1
                            num2=lista[pos]
                            num2_type, num2_value= num2
                            if num2_type not in ['DIRECTION']:
                                return False, pos
                            else: 
                                if pos+1 <len(lista):
                                    pos+=1
                                    parent2 = lista[pos]
                                    paren2_type, parent2_value= parent2
                                    if paren2_type not in ['PAREN']:
                                        return False, pos                                    
                        else: 
                            return False, pos
                else:
                    return False, pos
            elif num1_type== 'NUMBER':
                if pos+1 < len(lista):
                    pos+=1
                    coma=lista[pos]
                    coma_type, coma_value= coma
                    if coma_type not in ['COMMA']:
                        return False, pos
                    else:
                        if pos+1 < len(lista):
                            pos+=1
                            num2=lista[pos]
                            num2_type, num2_value= num2
                            if num2_type not in ['DIRECTION']:
                                return False, pos
                            else: 
                                if pos+1 <len(lista):
                                    pos+=1
                                    parent2 = lista[pos]
                                    paren2_type, parent2_value= parent2
                                    if paren2_type not in ['PAREN']:
                                        return False, pos                                    
                        else: 
                            return False, pos
                else:
                    return False, pos
            else:
                return False, pos
                
        else: 
            return False, pos
    
    return True, pos   
    
def main():
    with open('data/programa.txt', 'r') as file:
        program = file.read()

    tokens = tokenize(program)
    try:
        result = validate_program(tokens)
        if result == True:
            print("Yes")
        else:
            print("No")
    except SyntaxError as e:
        print(f"Syntax Error: {e}")

if __name__ == '__main__':
    main()





