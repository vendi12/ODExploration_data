#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
23 November 2017
.. codeauthor: svitlana vakulenko
    <svitlana.vakulenko@gmail.com>

Parsing the conversation transcripts with annotations

Annotation template: message_type>speaker_turn>message
e.g. greeting>E>Hi?

'''
import os
import re
import numpy as np

SAMPLE_TRANSCRIPT_FILE = 'data_gv_at/transcript1_1.txt'
# SAMPLE_TRANSCRIPT_FILE = 'opendataportal_at/transcript13_2.txt'
DIRS =['data_gv_at', 'opendataportal_at']
OPERATIONS = ['greeting()', 'set(keywords)', 'prompt(keywords)',
              'list(keywords)', 'success()', 'link(dataset)',
              'bool(data)', 'question(data)', 'top(keywords)', 'count(data)',
              'verify()', 'reject()', 'confirm()', 'prompt(link)', 'more()']


def parse_transcript(transcript_file, search_intent=None, max_n_vars=None):
    # parse concept type annotations
    concept_type = re.compile(']](.\*)')
    vars_counts = []
    turns_count = 0
    with open(transcript_file) as file:
        for line in file:
            try:
                intent, turn, message = line.split('>')
                if search_intent:
                    if intent == search_intent:
                        print message.strip()
                elif max_n_vars:
                        print turn, message.strip()
                        types = re.findall(concept_type, message)
                        concepts = [ctype.strip('*') for ctype in types if ctype not in ['H*', 'G*', '+*', '-*']]
                        # concepts = [ctype.strip('*') for ctype in types if ctype not in ['H*']]
                        if concepts and turn == 'A':
                        # if types and turn == 'A':
                            turns_count += 1
                            vars_count = len(concepts)
                            print "Variables:", vars_count
                            vars_counts.append(vars_count)
                            # print turn, message.strip()
                            # print concepts, vars_count
                            # print '\n'
                            # print turn, intent, message.strip(), types, vars_count
                        # else:
                        #     print turn, intent, message.strip()
                else:
                    # show the process template
                    print turn, intent
                
                if intent not in OPERATIONS:
                   print("Unknown intent" + intent)
            except:
                if '>' in line:
                    print("Error parsing line:")
                    print line
    print "Number of turns:", turns_count
    return vars_counts, turns_count


def test_parse_transcript():
    parse_transcript(SAMPLE_TRANSCRIPT_FILE)


def parse_all_transcripts(dirs=DIRS):
    for portal_dir in dirs:
        for file in os.listdir(portal_dir):
            if file[-4:] == '.txt':
                # print file
                parse_transcript('/'.join([portal_dir, file]))
                # print '\n'


def search_all_transcripts(intent='greeting()', dirs=DIRS):
    for portal_dir in dirs:
        for file in os.listdir(portal_dir):
            if file[-4:] == '.txt':
                # print file
                parse_transcript('/'.join([portal_dir, file]), intent)
                # print '\n'


def count_vars(dirs=DIRS):
    '''
    count the number of concept annotations per utterance
    '''
    n_vars = []
    n_turns = []
    for portal_dir in dirs:
        for file in os.listdir(portal_dir):
            if file[-4:] == '.txt':
                # print file
                nvars, nlines = parse_transcript('/'.join([portal_dir, file]), max_n_vars=1)
                n_vars.extend(nvars)
                n_turns.append(nlines)
                print "\n"
    print "\n"
    print sorted(n_vars)
    print "Average number of variables per utterance", reduce(lambda x, y: x + y, n_vars) / len(n_vars)
    print "Maximum number of variables per utterance", max(n_vars)

    print sorted(n_turns)
    print n_turns
    print "Average number of turns per dialog", reduce(lambda x, y: x + y, n_turns) / len(n_turns)
    print "Minimum number of turns per dialog", min(n_turns)
    print "Maximum number of turns per dialog", max(n_turns)


def produce_single_log(dirs=DIRS):
    index = 1
    for portal_dir in dirs:
        for file_name in os.listdir(portal_dir):
            if file_name[-4:] == '.txt':
                with open('/'.join([portal_dir, file_name])) as file:
                    for line in file:
                        try:
                            intent, turn, message = line.split('>')
                            # show the process template
                            print ';'.join([str(index), turn, intent])
                            
                            if intent not in OPERATIONS:
                               print("Unknown intent" + intent)
                        except:
                            if '>' in line:
                                print("Error parsing line:")
                                print line
                index += 1


def main():
    # search_all_transcripts(intent='list(keywords)')
    # parse_all_transcripts()
    count_vars()


if __name__ == '__main__':
    main()
