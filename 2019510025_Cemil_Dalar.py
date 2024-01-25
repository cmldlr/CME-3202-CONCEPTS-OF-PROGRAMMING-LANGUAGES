#global variables
FILE_LL = "ll.txt"
FILE_LR = "lr.txt"
FILE_INPUT = "input.txt"

"""With this assignment, I mainly applied the following assumptions. 
first assumption,the character length of nonterminals should not be longer than 1 . "A" can be but not "A'"
the second assumption is that the max length of the terminals should be 2
and I assumed "$" at the end of each input
"""

#variables for ll1 parsing
ll_matrix=[[]]
terminals_ll=dict()
nonterminals_ll=dict()

#variables for lr1 parsing
lr_matrix=[[]]
states_lr=dict()
action_goto_lr=dict()

#read ll.txt and transfer to data variable for terminal,nonterminal
def readtablell(filename,matrix,terminal,nonterminal):
  try:
   index_r=0;
   index_c=0;
   #find the size of ll_matrix. its a 2 dimensional array so firstly i have to decide size of it
   with open(filename, "r",encoding="utf-8") as s:    
     flag=True
     for str in s.readlines():
        pieces=str.split(";");
        if(flag):
          for i in pieces:
            index_c +=1
          flag=False 
        index_r+=1
     s.close()      
   #creating necessary variables example ll_matrix,terminals_ll,nonterminals_ll 
   with open(filename, "r",encoding="utf-8") as f:
    term_count=0 #terminal count
    nonterminal_count=1
    fname=filename.split(".")
    print( "Read "+ fname[0]+"(1) parsing table from file " + filename+ ".")
    flag=True
    flag2=False
    index_row=0
    index_col=0
    matrix = [[0 for i in range(index_c)] for j in range(index_r)] 
    for str in f.readlines():
       pieces=str.split(";");
       for i in pieces:
           i=i.replace(" ","")
           i=i.replace("\n","")
           i=i.replace("\t","")
           matrix[index_row][index_col]=i
           index_col +=1
           if flag:
            terminal[i]=term_count
            term_count +=1
           elif flag2:
              nonterminal[pieces[0].replace(" ","")]=nonterminal_count
              nonterminal_count +=1
              flag2=False
       index_row+=1
       index_col=0           
       flag=False
       flag2=True
    return matrix, terminal, nonterminal       
  except FileNotFoundError:
    print(filename +"file not found.")
  except Exception as e:
    print("Something went wrong.", e)
#read lr.txt and transfer to data variable for states,action_goto    
def readtablelr(filename,matrix,states,action_goto):
    try:
      index_r=0;
      index_c=0;
      #find the size of lr_matrix. its a 2 dimensional array so firstly i have to decide size of it
      with open(filename, "r",encoding="utf-8") as s:    
        flag=True
        for str in s.readlines():
          pieces=str.split(";");
          if(flag):
           for i in pieces:
            index_c +=1
          flag=False 
          index_r+=1
        s.close()
      #creating necessary variables example lr_matrix,states_lr,action_goto_lr  
      fname=filename.split(".")
      print( "Read "+ fname[0]+"(1) parsing table from file " + filename+ ".")
      matrix = [[0 for i in range(index_c)] for j in range(index_r)] 
      index_row=0
      index_col=0
      states_count=2
      action_goto_count=1
      with open (filename,"r",encoding="utf-8") as f:
        for row in f.readlines():
          column=row.split(";")
          for i in column:
            i=i.replace(" ","")
            i=i.replace("\n","");
            matrix[index_row][index_col]=i;
            if(index_row== 1 and index_col>=1):
              action_goto[i]=action_goto_count
              action_goto_count +=1
            if(index_col==0 and index_row>=2):
              i=i.split("_")
              states[i[1]]=states_count
              states_count+=1
            index_col+=1      
          index_row +=1
          index_col =0   
      return matrix,states,action_goto 
    except FileNotFoundError:
     print(filename +"file not found.")
    except Exception as e:
     print("Something went wrong.", e)
#read input txt and parsing the input
def readinputtxt():
 try:
   with open(FILE_INPUT, "r",encoding="utf-8") as f:
    print("Read input strings from file " + FILE_INPUT)    
    for rows in f.readlines():
      piece=rows.split(";")
      table=piece[0].replace(" ","");
      input=piece[1].replace("\n","");
      print(" ")
      if(table.upper()=="LL"):
        print("Processing input string "+input+" for "+FILE_LL+" parsing table.")
        ll1_parser(ll_matrix,terminals_ll,nonterminals_ll,input)
      elif(table.upper()=="LR"):
        print("Processing input string "+input+" for "+FILE_LR+" parsing table.")
        lr1_parser(lr_matrix,states_lr,action_goto_lr,input)
         
 except FileNotFoundError:
  print(FILE_INPUT +"file not found.")
 except Exception as e:
  print("Something went wrong.", e)

def get_ll_production(nonterminal, terminal):
    row = nonterminals_ll[nonterminal]
    col = terminals_ll[terminal]
    return ll_matrix[row][col]
  
#find the terminals in input string
def get_input_token(input_str,index,flag):
    if index < len(input_str):
        if input_str[index:index+2] in terminals_ll:
            temp_index=index
            index=index+2
            if(flag):
              return input_str[temp_index:index],index
            else:
              return input_str[temp_index:index]
        else:
            temp_index=index
            index=index+1
            if(flag):
              return input_str[temp_index:index],index
            else:
              return input_str[temp_index:index]
    elif input==len(input_str)-1:
        temp_index=index
        index=index+1
        if(flag):
          return input_str[temp_index:index],index
        else:
          return input_str[temp_index:index]
#ll(1) parser      
def ll1_parser(ll_matrix,terminals_ll,nonterminals_ll,input):
  #for the fint first_action in the parsing table     
  flag=False
  for row in ll_matrix:
    for element in row:
      print
      if(len(element)!=0 and element not in terminals_ll and element not in nonterminals_ll):
        first_action=element
        flag=True
      if(flag):
       break
  #format function for good outputs   
  print("{:>0} {:>20} {:>20} {:>25}"
        .format("NO",
                "STACK",
                "INPUT",
                "ACTION"))
  count=1    
  stack= ["$"] #stack
  index=0
  while True:
    if(count==1):
         print("{:>0} {:>20} {:>20} {:>25}"
        .format(count,
                ' '.join(stack),
                input,
                first_action))
         piece=first_action.split("->")
         if(piece[1]=="id"):
           stack.append(piece[1])
         elif piece[1] != "ϵ":
           for i in range(len(piece[1])-1, -1, -1):
              stack.append(piece[1][i])  
    else:     
      if stack[-1]=="$" and input[index] == "$": #finish condition
        print("{:>0} {:>20} {:>20} {:>25}"
        .format(count,
                ''.join(stack),
                input[index:],
                "Accepted"))
        return "Valid String!"
      elif stack[-1] not in terminals_ll: #nonterminal
        nonterminal=stack[-1]
        terminal=get_input_token(input, index,False)        
        if terminal not in terminals_ll :#Maybe it can include different types of terminals in the input, so we should check this.
          print("{:>0} {:>20} {:>20} {:>25}"
          .format(count,
                ''.join(stack),
                input[index:],
                "Rejected Invalid Terminal! "+ terminal ))
          return
        else : #terminal
          action=get_ll_production(nonterminal, terminal)
          if(action!=""):
             print("{:>0} {:>20} {:>20} {:>25}".
                      format(count,
                             ''.join(stack),
                            input[index:],
                            action))
             stack.pop()
             new_action = action.split("->")
             if new_action[1] == "id":
               stack.append(new_action[1])
             elif new_action[1] != "ϵ":
                for i in range(len(new_action[1])-1, -1, -1):
                    stack.append(new_action[1][i])                               
          else: #error message if there is no action/step
             print("{:>0} {:>20} {:>20} {:>60}"
                  .format(count,
                ''.join(stack),
                input[index:],
                      "REJECTED ("+nonterminal+" does not have an action/step for "+terminal+")")) 
             break            
      else: #terminal
        stack_top=stack[-1]
        temp_index=index
        terminal,index=get_input_token(input, index,True)
        if(terminal==stack_top):
          print("{:>0} {:>20} {:>20} {:>30}"
                      .format(count,
                              ''.join(stack),
                              input[temp_index:],
                              "Match and remove "+terminal))
          stack.pop()
        else:
            print("{:>0} {:>20} {:>20} {:>30}"
                      .format(count,
                              ''.join(stack),
                              input[temp_index:],
                              "Invalid Terminal"))
            return "Invalid Terminal"
    count +=1             
#lr(1) parsing
def lr1_parser(lr_matrix,states_lr,action_goto_lr,input):
  first_action=""
  for i in states_lr.keys():
      first_action=i
      break
  #find the first action in the parsing table  
  print("{:>0} {:>15} {:>8} {:>15} {:>18}"
        .format("NO",
                "STATE STACK",
                "READ",
                "INPUT",
                "ACTION"))
  count=1
  state_stack= [first_action] #state stack
  input_index=0
  while True:
    read=input[input_index]
    state_top=state_stack[-1]
    lr_product=lr_matrix[states_lr[state_top]][action_goto_lr[read]]
    if(lr_product.lower()=="accept"):
      print("{:>0} {:>15} {:>8} {:>15} {:>25}"
        .format(count,
                ' '.join(state_stack),
                read,
                input[input_index:],
                "Accepted"))
      return "Accepted"
    elif(lr_product==""): #error message for no action/step
      print("{:>0} {:>15} {:>8} {:>15} {:>60}"
        .format(count,
                ' '.join(state_stack),
                read,
                input[input_index:],
                "REJECTED (State "+state_top+" does not have an action/step for "+read+ ")"))
      return "Rejected"
    elif(lr_product.lower().startswith("state")):#find the next state 
      if(input_index==len(input)):#If we reach the end of the input and state actions will continue, it means that we do not have a long enough input.
            print("{:>0} {:>15} {:>8} {:>15} {:>25}"
              .format(count,
                ' '.join(state_stack),
                read,
                input,
                "Failed"))
            return "Failed"
      else:  
        find_next_state=lr_product.split("_");
        next_state=find_next_state[1]
        print("{:>0} {:>15} {:>8} {:>15} {:>25}"
        .format(count,
                ' '.join(state_stack),
                read,
                input,
                "Shift to state " + next_state))
        state_stack.append(next_state)
        input_index +=1
    else:
      find_reserve_element=lr_product.split("->");
      element0=find_reserve_element[0]
      element1=find_reserve_element[1]
      input=input.replace(element1,element0)    
      if(input.find(element0)!=-1):
        input_index=input.find(element0)
        for i in range (len(element1)):
          state_stack.pop()
        print("{:>0} {:>15} {:>8} {:>15} {:>25}"
         .format(count,
                ' '.join(state_stack),
                read,
                input,
                "Reverse " + lr_product))
      else:
        print("{:>0} {:>15} {:>8} {:>15} {:>25}"
         .format(count,
                ' '.join(state_stack),
                read,
                input,
                "Failed"))
        return "failed"
    count +=1 
     
ll_matrix, terminals_ll, nonterminals_ll = readtablell(FILE_LL, ll_matrix,terminals_ll,nonterminals_ll)  
lr_matrix,states_lr,action_goto_lr=readtablelr(FILE_LR, lr_matrix,states_lr,action_goto_lr)
readinputtxt()


    