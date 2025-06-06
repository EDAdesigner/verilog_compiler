
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'AMPERSAND AND ASSIGN BAR BUF CARET COLON COMMA DIVIDE DOT ENDMODULE EQUALS ID INPUT LBRACE LBRACKET LPAREN MINUS MODULE NAND NOR NOT NUMBER OR OUTPUT PLUS QUESTION RBRACE RBRACKET REG RPAREN SEMICOLON TILDE TIMES WIRE XNOR XORmodule_definition : MODULE ID LPAREN port_list RPAREN SEMICOLON module_items ENDMODULEport_list : port_list_itemsport_list_items : port_item\n                         | port_list_items COMMA port_itemport_item : ID\n                     | WIRE IDmodule_items : module_item\n                       | module_items module_item\n                       | emptymodule_item : input_declaration\n                      | output_declaration\n                      | wire_declaration\n                      | assign_statement\n                      | gate_instantiationinput_declaration : INPUT input_list SEMICOLON\n                           | INPUT WIRE input_list SEMICOLONinput_list : ID\n                     | input_list COMMA IDoutput_declaration : OUTPUT output_list SEMICOLON\n                              | OUTPUT WIRE output_list SEMICOLONoutput_list : ID\n                      | output_list COMMA IDwire_declaration : WIRE wire_list SEMICOLONwire_list : ID\n                    | wire_list COMMA IDassign_statement : ASSIGN ID EQUALS expression SEMICOLONexpression : term\n                     | expression PLUS term\n                     | expression MINUS term\n                     | expression AMPERSAND term\n                     | expression BAR term\n                     | expression CARET term\n                     | term QUESTION expression COLON expressionterm : ID\n               | NUMBER\n               | LPAREN expression RPAREN\n               | TILDE termempty :gate_instantiation : gate_type ID LPAREN signal_list RPAREN SEMICOLONgate_type : AND\n                    | OR\n                    | NOT\n                    | NAND\n                    | NOR\n                    | XOR\n                    | XNOR\n                    | BUFsignal_list : ID\n                      | signal_list COMMA ID'
    
_lr_action_items = {'MODULE':([0,],[2,]),'$end':([1,36,],[0,-1,]),'ID':([2,4,9,11,23,24,25,26,27,28,29,30,31,32,33,34,35,39,44,49,52,54,56,57,67,68,72,73,74,75,76,77,81,91,],[3,5,12,5,40,42,45,46,47,-40,-41,-42,-43,-44,-45,-46,-47,40,45,58,60,61,63,69,63,63,63,63,63,63,63,63,90,63,]),'LPAREN':([3,47,56,67,68,72,73,74,75,76,77,91,],[4,57,67,67,67,67,67,67,67,67,67,67,]),'WIRE':([4,11,13,15,16,17,18,19,20,21,22,23,25,37,48,51,53,59,62,71,89,],[9,9,24,24,-7,-9,-10,-11,-12,-13,-14,39,44,-8,-15,-23,-19,-16,-20,-26,-39,]),'COMMA':([5,7,8,12,14,38,40,41,42,43,45,50,55,58,60,61,69,70,90,],[-5,11,-3,-6,-4,49,-17,52,-24,54,-21,49,54,-18,-25,-22,-48,81,-49,]),'RPAREN':([5,6,7,8,12,14,63,65,66,69,70,78,79,82,83,84,85,86,88,90,92,],[-5,10,-2,-3,-6,-4,-34,-27,-35,-48,80,88,-37,-28,-29,-30,-31,-32,-36,-49,-33,]),'SEMICOLON':([10,38,40,41,42,43,45,50,55,58,60,61,63,64,65,66,79,80,82,83,84,85,86,88,92,],[13,48,-17,51,-24,53,-21,59,62,-18,-25,-22,-34,71,-27,-35,-37,89,-28,-29,-30,-31,-32,-36,-33,]),'ENDMODULE':([13,15,16,17,18,19,20,21,22,37,48,51,53,59,62,71,89,],[-38,36,-7,-9,-10,-11,-12,-13,-14,-8,-15,-23,-19,-16,-20,-26,-39,]),'INPUT':([13,15,16,17,18,19,20,21,22,37,48,51,53,59,62,71,89,],[23,23,-7,-9,-10,-11,-12,-13,-14,-8,-15,-23,-19,-16,-20,-26,-39,]),'OUTPUT':([13,15,16,17,18,19,20,21,22,37,48,51,53,59,62,71,89,],[25,25,-7,-9,-10,-11,-12,-13,-14,-8,-15,-23,-19,-16,-20,-26,-39,]),'ASSIGN':([13,15,16,17,18,19,20,21,22,37,48,51,53,59,62,71,89,],[26,26,-7,-9,-10,-11,-12,-13,-14,-8,-15,-23,-19,-16,-20,-26,-39,]),'AND':([13,15,16,17,18,19,20,21,22,37,48,51,53,59,62,71,89,],[28,28,-7,-9,-10,-11,-12,-13,-14,-8,-15,-23,-19,-16,-20,-26,-39,]),'OR':([13,15,16,17,18,19,20,21,22,37,48,51,53,59,62,71,89,],[29,29,-7,-9,-10,-11,-12,-13,-14,-8,-15,-23,-19,-16,-20,-26,-39,]),'NOT':([13,15,16,17,18,19,20,21,22,37,48,51,53,59,62,71,89,],[30,30,-7,-9,-10,-11,-12,-13,-14,-8,-15,-23,-19,-16,-20,-26,-39,]),'NAND':([13,15,16,17,18,19,20,21,22,37,48,51,53,59,62,71,89,],[31,31,-7,-9,-10,-11,-12,-13,-14,-8,-15,-23,-19,-16,-20,-26,-39,]),'NOR':([13,15,16,17,18,19,20,21,22,37,48,51,53,59,62,71,89,],[32,32,-7,-9,-10,-11,-12,-13,-14,-8,-15,-23,-19,-16,-20,-26,-39,]),'XOR':([13,15,16,17,18,19,20,21,22,37,48,51,53,59,62,71,89,],[33,33,-7,-9,-10,-11,-12,-13,-14,-8,-15,-23,-19,-16,-20,-26,-39,]),'XNOR':([13,15,16,17,18,19,20,21,22,37,48,51,53,59,62,71,89,],[34,34,-7,-9,-10,-11,-12,-13,-14,-8,-15,-23,-19,-16,-20,-26,-39,]),'BUF':([13,15,16,17,18,19,20,21,22,37,48,51,53,59,62,71,89,],[35,35,-7,-9,-10,-11,-12,-13,-14,-8,-15,-23,-19,-16,-20,-26,-39,]),'EQUALS':([46,],[56,]),'NUMBER':([56,67,68,72,73,74,75,76,77,91,],[66,66,66,66,66,66,66,66,66,66,]),'TILDE':([56,67,68,72,73,74,75,76,77,91,],[68,68,68,68,68,68,68,68,68,68,]),'QUESTION':([63,65,66,79,88,],[-34,77,-35,-37,-36,]),'PLUS':([63,64,65,66,78,79,82,83,84,85,86,87,88,92,],[-34,72,-27,-35,72,-37,-28,-29,-30,-31,-32,72,-36,72,]),'MINUS':([63,64,65,66,78,79,82,83,84,85,86,87,88,92,],[-34,73,-27,-35,73,-37,-28,-29,-30,-31,-32,73,-36,73,]),'AMPERSAND':([63,64,65,66,78,79,82,83,84,85,86,87,88,92,],[-34,74,-27,-35,74,-37,-28,-29,-30,-31,-32,74,-36,74,]),'BAR':([63,64,65,66,78,79,82,83,84,85,86,87,88,92,],[-34,75,-27,-35,75,-37,-28,-29,-30,-31,-32,75,-36,75,]),'CARET':([63,64,65,66,78,79,82,83,84,85,86,87,88,92,],[-34,76,-27,-35,76,-37,-28,-29,-30,-31,-32,76,-36,76,]),'COLON':([63,65,66,79,82,83,84,85,86,87,88,92,],[-34,-27,-35,-37,-28,-29,-30,-31,-32,91,-36,-33,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'module_definition':([0,],[1,]),'port_list':([4,],[6,]),'port_list_items':([4,],[7,]),'port_item':([4,11,],[8,14,]),'module_items':([13,],[15,]),'module_item':([13,15,],[16,37,]),'empty':([13,],[17,]),'input_declaration':([13,15,],[18,18,]),'output_declaration':([13,15,],[19,19,]),'wire_declaration':([13,15,],[20,20,]),'assign_statement':([13,15,],[21,21,]),'gate_instantiation':([13,15,],[22,22,]),'gate_type':([13,15,],[27,27,]),'input_list':([23,39,],[38,50,]),'wire_list':([24,],[41,]),'output_list':([25,44,],[43,55,]),'expression':([56,67,77,91,],[64,78,87,92,]),'term':([56,67,68,72,73,74,75,76,77,91,],[65,65,79,82,83,84,85,86,65,65,]),'signal_list':([57,],[70,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> module_definition","S'",1,None,None,None),
  ('module_definition -> MODULE ID LPAREN port_list RPAREN SEMICOLON module_items ENDMODULE','module_definition',8,'p_module_definition','verilog_parser.py',58),
  ('port_list -> port_list_items','port_list',1,'p_port_list','verilog_parser.py',69),
  ('port_list_items -> port_item','port_list_items',1,'p_port_list_items','verilog_parser.py',74),
  ('port_list_items -> port_list_items COMMA port_item','port_list_items',3,'p_port_list_items','verilog_parser.py',75),
  ('port_item -> ID','port_item',1,'p_port_item','verilog_parser.py',80),
  ('port_item -> WIRE ID','port_item',2,'p_port_item','verilog_parser.py',81),
  ('module_items -> module_item','module_items',1,'p_module_items','verilog_parser.py',96),
  ('module_items -> module_items module_item','module_items',2,'p_module_items','verilog_parser.py',97),
  ('module_items -> empty','module_items',1,'p_module_items','verilog_parser.py',98),
  ('module_item -> input_declaration','module_item',1,'p_module_item','verilog_parser.py',102),
  ('module_item -> output_declaration','module_item',1,'p_module_item','verilog_parser.py',103),
  ('module_item -> wire_declaration','module_item',1,'p_module_item','verilog_parser.py',104),
  ('module_item -> assign_statement','module_item',1,'p_module_item','verilog_parser.py',105),
  ('module_item -> gate_instantiation','module_item',1,'p_module_item','verilog_parser.py',106),
  ('input_declaration -> INPUT input_list SEMICOLON','input_declaration',3,'p_input_declaration','verilog_parser.py',110),
  ('input_declaration -> INPUT WIRE input_list SEMICOLON','input_declaration',4,'p_input_declaration','verilog_parser.py',111),
  ('input_list -> ID','input_list',1,'p_input_list','verilog_parser.py',116),
  ('input_list -> input_list COMMA ID','input_list',3,'p_input_list','verilog_parser.py',117),
  ('output_declaration -> OUTPUT output_list SEMICOLON','output_declaration',3,'p_output_declaration','verilog_parser.py',130),
  ('output_declaration -> OUTPUT WIRE output_list SEMICOLON','output_declaration',4,'p_output_declaration','verilog_parser.py',131),
  ('output_list -> ID','output_list',1,'p_output_list','verilog_parser.py',136),
  ('output_list -> output_list COMMA ID','output_list',3,'p_output_list','verilog_parser.py',137),
  ('wire_declaration -> WIRE wire_list SEMICOLON','wire_declaration',3,'p_wire_declaration','verilog_parser.py',150),
  ('wire_list -> ID','wire_list',1,'p_wire_list','verilog_parser.py',154),
  ('wire_list -> wire_list COMMA ID','wire_list',3,'p_wire_list','verilog_parser.py',155),
  ('assign_statement -> ASSIGN ID EQUALS expression SEMICOLON','assign_statement',5,'p_assign_statement','verilog_parser.py',163),
  ('expression -> term','expression',1,'p_expression','verilog_parser.py',167),
  ('expression -> expression PLUS term','expression',3,'p_expression','verilog_parser.py',168),
  ('expression -> expression MINUS term','expression',3,'p_expression','verilog_parser.py',169),
  ('expression -> expression AMPERSAND term','expression',3,'p_expression','verilog_parser.py',170),
  ('expression -> expression BAR term','expression',3,'p_expression','verilog_parser.py',171),
  ('expression -> expression CARET term','expression',3,'p_expression','verilog_parser.py',172),
  ('expression -> term QUESTION expression COLON expression','expression',5,'p_expression','verilog_parser.py',173),
  ('term -> ID','term',1,'p_term','verilog_parser.py',191),
  ('term -> NUMBER','term',1,'p_term','verilog_parser.py',192),
  ('term -> LPAREN expression RPAREN','term',3,'p_term','verilog_parser.py',193),
  ('term -> TILDE term','term',2,'p_term','verilog_parser.py',194),
  ('empty -> <empty>','empty',0,'p_empty','verilog_parser.py',203),
  ('gate_instantiation -> gate_type ID LPAREN signal_list RPAREN SEMICOLON','gate_instantiation',6,'p_gate_instantiation','verilog_parser.py',207),
  ('gate_type -> AND','gate_type',1,'p_gate_type','verilog_parser.py',216),
  ('gate_type -> OR','gate_type',1,'p_gate_type','verilog_parser.py',217),
  ('gate_type -> NOT','gate_type',1,'p_gate_type','verilog_parser.py',218),
  ('gate_type -> NAND','gate_type',1,'p_gate_type','verilog_parser.py',219),
  ('gate_type -> NOR','gate_type',1,'p_gate_type','verilog_parser.py',220),
  ('gate_type -> XOR','gate_type',1,'p_gate_type','verilog_parser.py',221),
  ('gate_type -> XNOR','gate_type',1,'p_gate_type','verilog_parser.py',222),
  ('gate_type -> BUF','gate_type',1,'p_gate_type','verilog_parser.py',223),
  ('signal_list -> ID','signal_list',1,'p_signal_list','verilog_parser.py',227),
  ('signal_list -> signal_list COMMA ID','signal_list',3,'p_signal_list','verilog_parser.py',228),
]
