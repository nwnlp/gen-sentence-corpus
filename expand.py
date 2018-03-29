import os
import random
def tag(char):
    if char == ')':
        return 'small_bracket'
    elif char == ']':
        return 'square_bracket'
    elif char == '}':
        return 'curly_bracket'
    else:
        return 'normal'

def simple_split(source_sent):
    bracket_cnt = 0
    copy_buffer = ''
    content = []
    for i in range(0, len(source_sent)):
        char = source_sent[i]
        if char == '[' or char == '(' or char == '{':
            bracket_cnt += 1
            if bracket_cnt==1:
                if copy_buffer:
                    content.append((copy_buffer, 'normal'))
                    copy_buffer = ''
                continue
        if char == ']' or char == ')' or char == '}':
            bracket_cnt -= 1
            if bracket_cnt == 0:
                content.append((copy_buffer,tag(char)))
                copy_buffer = ''
                continue
        copy_buffer += char
    if copy_buffer != '':
        content.append((copy_buffer,'normal'))
    return content
def expand_short_exp(short_exps):
    result = []
    for exp in short_exps:
        splits = simple_split(exp)
        for content in splits:
            if content[1] == 'normal':
                result.append(content[0])
            elif content[1] == 'square_bracket':
                result.append(exp.replace('[','').replace(']',''))
    return result


def combine(short_exps1, short_exps2):
    result = []
    short_exps1_list = short_exps1[0]
    short_exps2_list = short_exps2[0]
    for exp1 in short_exps1_list:
        for exp2 in short_exps2_list:
            exp = exp1+exp2
            result.append(exp)

    if short_exps1[1] == 'or':
        result.extend(short_exps2_list)
    if short_exps2[1] == 'or':
        result.extend(short_exps1_list)
    return (result, 'must')

def expand(source_sent):
    splits = simple_split(source_sent)
    result = []
    for content in splits:
        if content[1] == 'square_bracket':
            or_exps = content[0].split('|')
            result.append((or_exps,'or'))
        if content[1] == 'small_bracket':
            must_have_one = content[0].split('|')
            must_have_one = expand_short_exp(must_have_one)
            result.append((must_have_one, 'must'))
        if content[1] == 'curly_bracket':
            slot, slot_value = content[0].split('.')
            slot_value = slot_value.split('|')
            slot_value = expand_short_exp(slot_value)
            #slot_value  = '['+slot_value+'].'+slot
            slot_value = ['[' + value + '].(' + slot+')' for value in slot_value]
            result.append((slot_value, slot))
        if content[1] == 'normal':
            result.append(([content[0]], 'normal'))

    combined = result[0]
    for i in range(0, len(result) - 1):
        combined = combine(combined, result[i + 1])
    return combined[0]

if __name__ == '__main__':
    source_sent = '[我想|帮我|请](播[放]|打开)[一下|下]{app_name.有声读物|抖音}'
    sents = expand(source_sent)
    print('\n'.join(sents))