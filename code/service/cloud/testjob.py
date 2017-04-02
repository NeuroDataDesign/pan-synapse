import sys
import boto3

def testJob(txtfile):
    with open(txtfile, "r") as f:
        newFile = open("output.txt", "w")
        newFile.write(str(f.readline()) + "WORLD")
        newFile.close()
    return newFile.name

def getData(key, datadir):
    s3 = boto3.resource('s3')
    filename = datadir + '/' + key
    data = s3.meta.client.download_file('nddtestbucket', key, filename)
    return filename

def uploadResults(key, results):
    s3 = boto3.resource('s3')
    key = key.split(".")[0] + 'results' + '.txt'
    data = open(results, 'rb')
    s3.Bucket('nddtestbucketresults').put_object(Key=key, Body=data)
    return key

output = testJob(getData(sys.argv[1], 'data'))
uploadResults(sys.argv[1], output)
