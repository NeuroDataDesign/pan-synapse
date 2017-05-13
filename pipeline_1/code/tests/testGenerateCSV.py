import sys
sys.path.insert(0, '../functions')
import runPipeline as pipe

testList = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
pipe.generateCSV('__TEST__', testList)
print 'Test CSV generated in /service/static/results'
print 'Verify contents are:\n1, 2, 3\n4, 5, 6\n7, 8, 9'
