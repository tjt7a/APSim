import automata as atma
from automata.automata_network import compare_input, compare_strided, StartType
from anml_zoo import anml_path,input_path,AnmalZoo
from tqdm import tqdm
import pickle
from utility import minimize_automata, multi_byte_stream, get_equivalent_symbols, replace_equivalent_symbols
import math
from automata.HDL.hdl_generator import test_compressor


snort50 = pickle.load(open('Snort1-50.pkl'))

for s in snort50:

    stride_dict_list = []
    for i in range(4):

        symbol_dict, symbol_dictionary_list = get_equivalent_symbols([s])

        if i == 0:
            initial_dic = symbol_dict
            initial_bits = int(math.ceil(math.log(max(initial_dic.values()), 2)))
            width_list=[initial_bits]
            test_compressor(original_width=8,
                            byte_trans_map=initial_dic,
                            byte_map_width=initial_bits,
                            translation_list=[],
                            idx=0,
                            width_list=[],
                            initial_width=initial_bits,
                            output_width=initial_bits)
            replace_equivalent_symbols(symbol_dictionary_list, [s])
        else:
            stride_dict_list.append(symbol_dict)
            width_list.append(int(math.ceil(math.log(max(symbol_dict.values()), 2))))
            print len(set(symbol_dict.values()))
            replace_equivalent_symbols(symbol_dictionary_list, [s])
            test_compressor(original_width=pow(2, i) * 8,
                            byte_trans_map=initial_dic,
                            byte_map_width=initial_bits,
                            translation_list=stride_dict_list,
                            idx=0,
                            width_list=width_list,
                            initial_width=pow(2,i) * initial_bits,
                            output_width=width_list[-1])

        s = s.get_single_stride_graph()
        s.make_homogenous()
        minimize_automata(s)



for i in range(3):
    new_total =[]
    for s in total_atms:
        s = s.get_single_stride_graph()
        s.make_homogenous()
        minimize_automata(s)
        new_total.append(s)

    total_atms = new_total

    symbol_dict, symbol_dictionary_list = get_equivalent_symbols(total_atms)
    print len(set(symbol_dict.values()))
    replace_equivalent_symbols(symbol_dictionary_list, total_atms)













