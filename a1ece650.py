import re

def numbers_check(string):
        for numbers in re.findall("[(][^)]*[)]", string):
            if len(re.findall("[-+]?\d+[\.]?\d*[eE]?[-+]?\d*", numbers)) == 2:
                continue
            else:
                return 0
        return 1
    
def bracket_check(string):
        if "(" not in string or ")" not in string:
            return 0
        count = 0
        for i in string:
            if i == "(":
                count += 1
            elif i == ")":
                if count == 0:
                    return 0
                count -= 1
        return count==0
    
def extractNumbers(string):
    new_vertex = []
    
    string = string.replace(" ", "")
    string = string.replace(")(", ",")
    string = string.replace(")", "")
    string = string.replace("(", "")
    string = string.replace(",", " ")
    string = string.split(' ')
    
    x = string[0::2]
    y = string[1::2]

    for i in range(len(x)):
        x[i] = float(x[i])
        y[i] = float(y[i])
    return zip(x,y)

def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       return None

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y

def poly_intersection(poly1, poly2):
    
    length = len(poly1) + len(poly2)
    for k in range(length):
        for i, p1_first_point in enumerate(poly1[:-1]):
            p1_second_point = poly1[i + 1]

            for j, p2_first_point in enumerate(poly2[:-1]):
                p2_second_point = poly2[j + 1]

                if line_intersection((p1_first_point, p1_second_point), (p2_first_point, p2_second_point)):
                        intersect.append([p1_second_point])
                        intersect.append([line_intersection((p1_first_point, p1_second_point), (p2_first_point, p2_second_point))])
                        intersect.append([p2_second_point])
                        global_edges.append([p1_second_point, line_intersection((p1_first_point, p1_second_point), (p2_first_point, p2_second_point)), p2_second_point])
##        print ("result: ", (intersect)) #test#
##        print "global edges: ",global_edges
        return (intersect)               
                

    return None

def plotVertexandEdge():
        temp_dic = street_coord_dic
        values_coords = []
        result = []
        flag = 0
        for i in temp_dic:
                values_coords.append(temp_dic[i])
        #print (values_coords)
        #print len(values_coords)
        if(len(values_coords) == 1):
                flag = 1
        elif(len(values_coords) > 2):
                flag = 0
                for i in range(len(values_coords)):
                        for j in range (i+1, len(values_coords)):
                                result = poly_intersection(values_coords[i-1], values_coords[j])
        if(len(values_coords)== 2):
                flag = 0
                for i in range(len(values_coords)):
                        result = poly_intersection(values_coords[i-1], values_coords[i])
        
        if result not in common_vertex:
                common_vertex.extend(result)
##        print ("result: ", (result)) #test#
##        print ("common vertex: ", (common_vertex)) #test#
        
        new_intersection_line = []
        tmp = []
    
        for j in range(len(result) - 1):
                for i in range(j+1, len(result)):
                    
                        if result[j][0] == result[i][0] and result[j][-1] == result[i][-1]:
                                for p in result[j]:
                                    tmp.append(p)
                                for q in result[i]:
                                    if q not in tmp:
                                        tmp.append(q)
                                    else:
                                        continue
                    
                                del result[i]
                                del result[j]
                
                                new_intersection_line.append(sorted(tmp))
                
                                tmp = []
                                break
                
                if j == len(result) - 2:
                    break
        
        for i in new_intersection_line:
                result.append(i)
    
        pos = []
        for i in result:
                for j in i:
                    if j not in pos:
                        pos.append(j)
                        
        output_vertices = {}
        for i in pos:
                output_vertices[pos.index(i)] = i

##        print ("output: ", output_vertices) #test#

        if flag==1:
                print "V = {"
                
                print "}"
        else:
                print "V = {"
                for key, value in output_vertices.items():
                        print ' ' + str(key) + ': '+'('+ str("{0:.2f}".format(value[0])) + ',' + str("{0:.2f}".format(value[1])) + ')'
                print "}"
                
        final_edges = []
        
        for i in range(len(global_edges)):
                for j in range(len(global_edges[i])-1): 
                        first = list(output_vertices.keys())[list(output_vertices.values()).index(global_edges[i][j])]
                        second = list(output_vertices.keys())[list(output_vertices.values()).index(global_edges[i][j+1])]
            
                        if first != second:
                                res = (first, second) if first < second else (second, first)
                                final_edges.append(res)
   
        final_edges = list(set(final_edges))
##        print ("final edges: ", final_edges)

        print "E = {"
        for i in range(len(final_edges)): 
                if i == len(final_edges)-1:
                        print ' <' + str(final_edges[i][0]) + ',' + str(final_edges[i][1]) + '>'
                else:
                        print ' <' + str(final_edges[i][0]) + ',' + str(final_edges[i][1]) + '>,'
            
        print '}'
                
sts_coord = []
common_vertex = []
street_coord_dic = {}
global_edges = []
intersect = []

def main():
    ### YOUR MAIN CODE GOES HERE

    ### sample code to read from stdin.
    ### make sure to remove all spurious print statements as required
    ### by the assignment

        while True:
            command = raw_input("Enter input: ")

            if 'g' == command.strip(''):
                plotVertexandEdge()
        
            elif '"' not in command:
                print "Error: Invalid command. Try again"
    
            elif '"' in command and len(command.split('"'))==3:
                split_command = command.split('"')

##        print split_command
        
        ##street name check##    
                if all(x.isalpha() or x.isspace() for x in split_command[1]) and split_command[1] != "":
                    valid_name = 1
                else:
                    valid_name = 0
        ##########################
                
                if bracket_check(split_command[2]) and numbers_check(split_command[2]) and " " in split_command[2] and valid_name==1:
                        sts_coord = extractNumbers(split_command[2])
                        for i in sts_coord:
                                if i not in common_vertex:
                                        common_vertex.append(i)
                            
                        if "a " in split_command[0] and len(split_command)==3:
                                if split_command[1].lower() not in street_coord_dic:
                                        street_coord_dic[split_command[1].lower()] = sts_coord
                                else:
                                        print "Error: Street name already exists"
                        elif "c " in split_command[0] and len(split_command)==3:
                                if split_command[1].lower() in street_coord_dic:
                                        street_coord_dic[split_command[1].lower()] = sts_coord
                                else:
                                        print "Error: Street name does not exist"
                        else:
                                print "Error: Command is not valid"
            
            #Test#
##            print "valid input"
##            print sts_coord
##            print street_coord_dic
            ######
                elif "r " in split_command[0] and valid_name==1:
                        del global_edges[:]
                        if split_command[1].lower() in street_coord_dic:
                                del street_coord_dic[split_command[1].lower()]
                        else:
                                print "Error: Street does not exist"
                else:
                        print "Error: Invalid command"
            else:
                    print "Error: Invalid command format"

if __name__ == '__main__':
    main()
