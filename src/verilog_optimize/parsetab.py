
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'AMPERSAND AND ASSIGN BUF COMMA ENDMODULE EQUALS ID INPUT LPAREN MINUS MODULE NAND NOR NOT NUMBER OR OR_OP OUTPUT PLUS RPAREN SEMICOLON TILDE WIRE XNOR XOR XOR_OPmodule_definition : MODULE ID LPAREN port_list RPAREN SEMICOLON declarations statements ENDMODULEport_list : port_item\n                    | port_item COMMA port_listport_item : IDdeclarations : declarations declaration\n                       | declaration\n                       | emptydeclaration : input_declaration\n                      | output_declaration\n                      | wire_declarationinput_declaration : INPUT port_list SEMICOLONoutput_declaration : OUTPUT port_list SEMICOLONwire_declaration : WIRE port_list SEMICOLONstatements : statements statement\n                     | statement\n                     | emptystatement : gate_instantiation\n                    | assign_statementgate_instantiation : gate_type ID LPAREN signal_list RPAREN SEMICOLONgate_type : AND\n                    | OR\n                    | NOT\n                    | NAND\n                    | NOR\n                    | XOR\n                    | XNOR\n                    | BUFsignal_list : ID\n                      | ID COMMA signal_listassign_statement : ASSIGN ID EQUALS expression SEMICOLONexpression : term\n                     | expression PLUS term\n                     | expression AMPERSAND term\n                     | expression OR_OP term\n                     | expression XOR_OP term\n                     | TILDE termterm : ID\n               | NUMBER\n               | LPAREN expression RPARENempty :'
    
_lr_action_items = {'MODULE':([0,],[2,]),'$end':([1,40,],[0,-1,]),'ID':([2,4,9,18,19,20,27,28,29,30,31,32,33,34,35,36,47,48,54,56,57,60,61,62,63,],[3,5,5,5,5,5,42,43,-20,-21,-22,-23,-24,-25,-26,-27,49,51,51,51,49,51,51,51,51,]),'LPAREN':([3,42,48,54,56,60,61,62,63,],[4,47,56,56,56,56,56,56,56,]),'COMMA':([5,7,49,],[-4,9,57,]),'RPAREN':([5,6,7,11,49,50,51,53,55,64,65,66,68,69,70,71,72,],[-4,8,-2,-3,-28,58,-37,-31,-38,-36,72,-29,-32,-33,-34,-35,-39,]),'SEMICOLON':([5,7,8,11,37,38,39,51,52,53,55,58,64,68,69,70,71,72,],[-4,-2,10,-3,44,45,46,-37,59,-31,-38,67,-36,-32,-33,-34,-35,-39,]),'INPUT':([10,12,13,14,15,16,17,22,44,45,46,],[18,18,-6,-7,-8,-9,-10,-5,-11,-12,-13,]),'OUTPUT':([10,12,13,14,15,16,17,22,44,45,46,],[19,19,-6,-7,-8,-9,-10,-5,-11,-12,-13,]),'WIRE':([10,12,13,14,15,16,17,22,44,45,46,],[20,20,-6,-7,-8,-9,-10,-5,-11,-12,-13,]),'ASSIGN':([10,12,13,14,15,16,17,21,22,23,24,25,26,41,44,45,46,59,67,],[-40,28,-6,-7,-8,-9,-10,28,-5,-15,-16,-17,-18,-14,-11,-12,-13,-30,-19,]),'AND':([10,12,13,14,15,16,17,21,22,23,24,25,26,41,44,45,46,59,67,],[-40,29,-6,-7,-8,-9,-10,29,-5,-15,-16,-17,-18,-14,-11,-12,-13,-30,-19,]),'OR':([10,12,13,14,15,16,17,21,22,23,24,25,26,41,44,45,46,59,67,],[-40,30,-6,-7,-8,-9,-10,30,-5,-15,-16,-17,-18,-14,-11,-12,-13,-30,-19,]),'NOT':([10,12,13,14,15,16,17,21,22,23,24,25,26,41,44,45,46,59,67,],[-40,31,-6,-7,-8,-9,-10,31,-5,-15,-16,-17,-18,-14,-11,-12,-13,-30,-19,]),'NAND':([10,12,13,14,15,16,17,21,22,23,24,25,26,41,44,45,46,59,67,],[-40,32,-6,-7,-8,-9,-10,32,-5,-15,-16,-17,-18,-14,-11,-12,-13,-30,-19,]),'NOR':([10,12,13,14,15,16,17,21,22,23,24,25,26,41,44,45,46,59,67,],[-40,33,-6,-7,-8,-9,-10,33,-5,-15,-16,-17,-18,-14,-11,-12,-13,-30,-19,]),'XOR':([10,12,13,14,15,16,17,21,22,23,24,25,26,41,44,45,46,59,67,],[-40,34,-6,-7,-8,-9,-10,34,-5,-15,-16,-17,-18,-14,-11,-12,-13,-30,-19,]),'XNOR':([10,12,13,14,15,16,17,21,22,23,24,25,26,41,44,45,46,59,67,],[-40,35,-6,-7,-8,-9,-10,35,-5,-15,-16,-17,-18,-14,-11,-12,-13,-30,-19,]),'BUF':([10,12,13,14,15,16,17,21,22,23,24,25,26,41,44,45,46,59,67,],[-40,36,-6,-7,-8,-9,-10,36,-5,-15,-16,-17,-18,-14,-11,-12,-13,-30,-19,]),'ENDMODULE':([10,12,13,14,15,16,17,21,22,23,24,25,26,41,44,45,46,59,67,],[-40,-40,-6,-7,-8,-9,-10,40,-5,-15,-16,-17,-18,-14,-11,-12,-13,-30,-19,]),'EQUALS':([43,],[48,]),'TILDE':([48,56,],[54,54,]),'NUMBER':([48,54,56,60,61,62,63,],[55,55,55,55,55,55,55,]),'PLUS':([51,52,53,55,64,65,68,69,70,71,72,],[-37,60,-31,-38,-36,60,-32,-33,-34,-35,-39,]),'AMPERSAND':([51,52,53,55,64,65,68,69,70,71,72,],[-37,61,-31,-38,-36,61,-32,-33,-34,-35,-39,]),'OR_OP':([51,52,53,55,64,65,68,69,70,71,72,],[-37,62,-31,-38,-36,62,-32,-33,-34,-35,-39,]),'XOR_OP':([51,52,53,55,64,65,68,69,70,71,72,],[-37,63,-31,-38,-36,63,-32,-33,-34,-35,-39,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'module_definition':([0,],[1,]),'port_list':([4,9,18,19,20,],[6,11,37,38,39,]),'port_item':([4,9,18,19,20,],[7,7,7,7,7,]),'declarations':([10,],[12,]),'declaration':([10,12,],[13,22,]),'empty':([10,12,],[14,24,]),'input_declaration':([10,12,],[15,15,]),'output_declaration':([10,12,],[16,16,]),'wire_declaration':([10,12,],[17,17,]),'statements':([12,],[21,]),'statement':([12,21,],[23,41,]),'gate_instantiation':([12,21,],[25,25,]),'assign_statement':([12,21,],[26,26,]),'gate_type':([12,21,],[27,27,]),'signal_list':([47,57,],[50,66,]),'expression':([48,56,],[52,65,]),'term':([48,54,56,60,61,62,63,],[53,64,53,68,69,70,71,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> module_definition","S'",1,None,None,None),
  ('module_definition -> MODULE ID LPAREN port_list RPAREN SEMICOLON declarations statements ENDMODULE','module_definition',9,'p_module_definition','verilog_parser.py',42),
  ('port_list -> port_item','port_list',1,'p_port_list','verilog_parser.py',46),
  ('port_list -> port_item COMMA port_list','port_list',3,'p_port_list','verilog_parser.py',47),
  ('port_item -> ID','port_item',1,'p_port_item','verilog_parser.py',54),
  ('declarations -> declarations declaration','declarations',2,'p_declarations','verilog_parser.py',58),
  ('declarations -> declaration','declarations',1,'p_declarations','verilog_parser.py',59),
  ('declarations -> empty','declarations',1,'p_declarations','verilog_parser.py',60),
  ('declaration -> input_declaration','declaration',1,'p_declaration','verilog_parser.py',64),
  ('declaration -> output_declaration','declaration',1,'p_declaration','verilog_parser.py',65),
  ('declaration -> wire_declaration','declaration',1,'p_declaration','verilog_parser.py',66),
  ('input_declaration -> INPUT port_list SEMICOLON','input_declaration',3,'p_input_declaration','verilog_parser.py',70),
  ('output_declaration -> OUTPUT port_list SEMICOLON','output_declaration',3,'p_output_declaration','verilog_parser.py',75),
  ('wire_declaration -> WIRE port_list SEMICOLON','wire_declaration',3,'p_wire_declaration','verilog_parser.py',80),
  ('statements -> statements statement','statements',2,'p_statements','verilog_parser.py',85),
  ('statements -> statement','statements',1,'p_statements','verilog_parser.py',86),
  ('statements -> empty','statements',1,'p_statements','verilog_parser.py',87),
  ('statement -> gate_instantiation','statement',1,'p_statement','verilog_parser.py',91),
  ('statement -> assign_statement','statement',1,'p_statement','verilog_parser.py',92),
  ('gate_instantiation -> gate_type ID LPAREN signal_list RPAREN SEMICOLON','gate_instantiation',6,'p_gate_instantiation','verilog_parser.py',96),
  ('gate_type -> AND','gate_type',1,'p_gate_type','verilog_parser.py',109),
  ('gate_type -> OR','gate_type',1,'p_gate_type','verilog_parser.py',110),
  ('gate_type -> NOT','gate_type',1,'p_gate_type','verilog_parser.py',111),
  ('gate_type -> NAND','gate_type',1,'p_gate_type','verilog_parser.py',112),
  ('gate_type -> NOR','gate_type',1,'p_gate_type','verilog_parser.py',113),
  ('gate_type -> XOR','gate_type',1,'p_gate_type','verilog_parser.py',114),
  ('gate_type -> XNOR','gate_type',1,'p_gate_type','verilog_parser.py',115),
  ('gate_type -> BUF','gate_type',1,'p_gate_type','verilog_parser.py',116),
  ('signal_list -> ID','signal_list',1,'p_signal_list','verilog_parser.py',120),
  ('signal_list -> ID COMMA signal_list','signal_list',3,'p_signal_list','verilog_parser.py',121),
  ('assign_statement -> ASSIGN ID EQUALS expression SEMICOLON','assign_statement',5,'p_assign_statement','verilog_parser.py',188),
  ('expression -> term','expression',1,'p_expression','verilog_parser.py',211),
  ('expression -> expression PLUS term','expression',3,'p_expression','verilog_parser.py',212),
  ('expression -> expression AMPERSAND term','expression',3,'p_expression','verilog_parser.py',213),
  ('expression -> expression OR_OP term','expression',3,'p_expression','verilog_parser.py',214),
  ('expression -> expression XOR_OP term','expression',3,'p_expression','verilog_parser.py',215),
  ('expression -> TILDE term','expression',2,'p_expression','verilog_parser.py',216),
  ('term -> ID','term',1,'p_term','verilog_parser.py',243),
  ('term -> NUMBER','term',1,'p_term','verilog_parser.py',244),
  ('term -> LPAREN expression RPAREN','term',3,'p_term','verilog_parser.py',245),
  ('empty -> <empty>','empty',0,'p_empty','verilog_parser.py',252),
]
