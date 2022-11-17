from datapros import metaGenePlot

test = metaGenePlot('RPKM_alignments.sam','saccharomyces_cerevisiae.gff','gene', 0) #single para, if single = true - provide input for left or right end (if exists)

test.plot( 3,1000)

# one = 10 
# two = False 
# three = True 
# if one>=10 and two or three:
#     print('True')
# else:
#     print('Fasle ')
# labels = []
# with open('RPKM_alignments.sam', 'r') as samFile:
#     lines = samFile.readlines() 
# samFile.close()
# for line in lines:
#     cols = line.split('\t')
    
#     print(cols, len(cols))
#             for line in samFile:
#                 cols = line.split('\t')
#                 print(line)
#                 if len(cols)>=10 and cols[2] not in labels :
#                     labels.append(cols[2])
          
# print(labels)
 