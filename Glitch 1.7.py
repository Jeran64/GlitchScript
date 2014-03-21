#version 1.7.1
#to use this, put script in a folder next to the desired file. file should be called "out0" it will be kept as the original, and iterative copies will be made.
import random
import os.path
a=1 #start at one, so it can look for the file out0
b=0
c=0
x=0

minswapchunk=16384;# smallest swap chunk in bytes  i found that this feature is BEST used on uncompressed files. larger swaps are better.
maxswapchunk=32768;# number of bytes that the swap chunk can take at a maximum
chunkswapchance=.2;# chance that the swappage will be a chunk swap. set to 1 for JUST chunk swaps. set to 0.0 for no swappage/
reversechunkchance=.2# dependent on chunk swap chance. will only run a likelyhood of a chunkreverse if chunk swap was selected to happen that iteration. this is because reversing cannot happen unless a chunk is selected anyway.
chunksplicechance=1.0## dependent ont he chunkswap chance.  this is the likely hood of bringing forigen chunks. keep this low. once a chunk is brought in and over written, it sticks around. you can easily end up having your original image taken over by the spliced image.
    #a note about file splicing. if you want the data you import to be visible in an image, make sure that the files are both uncompressed, and are the same width. otherwise, what will happen is that the images will be read, and they will be offset, since they dont mach. it will create strong diagonal lines if you dont, so if thats what you are going for, then bam.power to you.
maxstride=1 #edite the bytes in chunks on maxstrde bytes. this is for the RANDOM bytes, not chunk swapping.
everynbytes=10#change this to only alter every n bytes. could be useful
everynbytesoffset=0#offset the every n bytes.
generatedimages=4 #use this to iterate an image. this will generate a file that has been corrupted, then the next iteration will load the previous one, and try to corrupt that. very useful for showing progression.
editedbytes=1# number of bytes/chunks to be destroyed. i find a great rule of thumb is to edit about 1/1000th the nubmer of total bytes in the image. some file formats can take more abuse than others.
headerlimiter=10000#this is the number of "protected" bytes at the start of the file. most files have header bytes that tell readers what they are and the properties of the file. its best to avoid damaging the header bytes, so they file has a better chance of being readable.
enderlimiter=20#number of protected bytes from teh end of the file. use this in combo witht he  header limiter to only change a specific range of bytes.
fileformat=".gif"#change this to match the file format of what you are changing.
splicesourcename="splicesource"#you probably dont need to change this. it will look for a file with this name and the file extension as specified above. the file formats should match, but they dont HAVE to, but im going to force you to.

if(os.path.isfile(splicesourcename+fileformat)):##returns true if a file actually exists in the directory that is the splice file.
    print "detected splice file."
else:
    print "no splice file detected. setting chance of splicing to 0.0"
    chunksplicechance=0 ##this feature will prevent errors.

for a in range(1,generatedimages+1):# number of image steps
    Filebits=open("out"+str(a-1)+fileformat, "rb")# this will open the previous one.
    DataList=Filebits.read()
    print len(DataList) #see if the list is populated
    s=list(DataList)#convert the read data into a list of bytes
    b=0#reset b so it can loop again. 
    if(maxswapchunk+headerlimiter>len(s)-enderlimiter):##check for the possibility of an out of bounds.
        print "Caught Error. Check options for bounds of chunks. Adjust so that they are not bigger than the maximum file"
    if(minswapchunk+headerlimiter>len(s)-enderlimiter):##check for the possibility of an out of bounds.
        print "Caught Error. Check options for bounds of chunks. Adjust so that they are not bigger than the maximum file"
    if(minswapchunk>maxswapchunk):##check for the possibility of an out of bounds.
        print "Caught Error. Check options for bounds of chunks. Adjust so that the mix is less than max."
    for b in range(0,editedbytes):#this is the number of times it goes and alters a byte in the file. 
        if random.uniform(0.0,1.0)<=chunkswapchance:#do chunk swap.
            firstchunkstart=random.randint(headerlimiter, len(s)-enderlimiter-maxswapchunk)# make sure we dont pick a chunk length that can encroach into the protected areas
            chunklength=random.randint(minswapchunk,maxswapchunk)
            if random.uniform(0.0,1.0)>reversechunkchance: #this is a chunk swap, as opposed to a reversal. by using greaterthan, we effectivly do a not lessthan or equal to. we only want regular chunk swapping if there reversing has not been selected.
                if random.uniform(0.0,1.0)<chunksplicechance:##if this gets picked, then we are going to splice a 2nd files data in! how exciting
                    ###i KNOW this is a terrible and inefficient way of doing this. i should not be loading the WHOLE damn image every time i splice. this will be improved in a later version.
                    Filebitstwo=open(splicesourcename+fileformat, "rb")# this will open the file flagged as the splice import.
                    DataListtwo=Filebitstwo.read()#save dat stuff.
                    print len(DataListtwo) #see if the list is populated
                    r=list(DataListtwo)#we can now read the bytes of our splice image as usual.  
                    splicechunk=random.randint(0,len(r))# pick the 2nd chunks starting location #fun fact, so, since we are putting this data into the current image, and we are just reading, and not writing, we dont have to worry about stupid things like protecting the file headers.
                    for q in range(0,chunklength):##for the length of the chunk, start exchanging values. notice that this
                        ##q=q%len(r)#if the file requested is outside the image file bounds, just loop back around.
                        s[firstchunkstart+q],r[(splicechunk+q)%len(r)]=r[(splicechunk+q)%len(r)],s[firstchunkstart+q]# this is the python swap command. we just exchange the values make sure that when we are looking for data in the spliced image that if the data we need is out of the bounds of the image, that we just loop around the image file using the % function/
                    print "progress:"+str(float(b)/float(editedbytes))+" splicing chunk #1 @"+str(firstchunkstart)+" swapping 2nd chunk at "+str(splicechunk)+" and swapping "+str(chunklength)+" bytes on picture "+str(a)
                else:##this means we didnt choose to instead splice the file.
                    secondchunkstart=random.randint(headerlimiter, len(s)-enderlimiter-maxswapchunk)# since we picked a chunk SWAP, pick the 2nd spot.
                    for u in range(0,chunklength):##for the length of the chunk, start exchanging values.
                        s[firstchunkstart+u],s[secondchunkstart+u]=s[secondchunkstart+u],s[firstchunkstart+u]# this is the python swap command. we just exchange the values
                    print "progress:"+str(float(b)/float(editedbytes))+" chunk #1 @"+str(firstchunkstart)+" swapping 2nd chunk at "+str(secondchunkstart)+" and swapping "+str(chunklength)+" bytes on picture "+str(a)
            else:##this is where the reversing happens.
                for v in range(0,chunklength/2): ##make sure you only do half the length. otherwise you will reverse whats already been reversed.
                    s[firstchunkstart+v],s[firstchunkstart+chunklength-v]=s[firstchunkstart+chunklength-v],s[firstchunkstart+v]
                print "progress:"+str(float(b)/float(editedbytes))+" reversing chunk @"+str(firstchunkstart)+" of length "+str(chunklength)+" bytes, to help make file "+str(a)
        else:#dont do a chunk swap. just do a single byte.
            c=random.randint(headerlimiter, len(s)-enderlimiter )##set c to a initial value, so we can start the testing loop.
            while c%everynbytes != 0:#this is a REALLY dumb hack. just keep drawing randimb numbers over and over again untill one is within the every n bytes category. i could make this more efficient with math, but fuck that, i iwll do it later in the optimization phase.
                print str(c%everynbytes)
                c=random.randint(headerlimiter, len(s)-enderlimiter )
            c+=everynbytesoffset# offset our chosen value to reach various bytes that would not other wise be reachable byt the everty nth byte function.
            x=0#reset x so we can execute the loop again
            for x in range(0,maxstride):#change from 1 byte to 8 in a row # this is a feature of altering strides of data, for the sake of it.
                s[c+x]=chr(random.randint(0,255))#sets a random byte location to a random byte value
            print "progress:"+str(float(b)/float(editedbytes))+" byte #"+str(c)+" and trailing for "+str(maxstride)+" on file "+str(a)
    DataList="".join(s)#reconstitute our list into a string file, since thats how files are loadedinto script memory
    with open('out'+str(a)+fileformat,"wb") as f: #write the file.
        f.write(DataList)
    f.close()# close the file. i dont think we need it anymore.
    
    print "Output to out"+str(a)+str(fileformat)#say that we did it.
    a=a+1

##version 1.2. now featuring more spelling errors, more code, and more confusing ideas.
## change long
    # added in more comments,
    # added in the chunk swapping feature. this will switch around large chunks of bytes. not sure if its useful, but it does stuff!.
    ## added in data chunk reversing.
    # replaced while loops with for loops. i used while loops at first because i was lazy, and didnt feel like looking up for loops in python, becase python does EVERYthing so weird.
    #added in data splicing.
##future log.
    ## make things percentage based. that way we can not worry about some files being smaller or bigger.
    ## add in a only-edit-every-x-bytes? (not comptatible witht chunking)
    
#this is being released as a public domain script, no attribution nessicary.
#please understand the risk of this code. it is intentionally destroying bytes.
#if you do not know the harm it can do, you should not be using this.
#I cannot in any way be held responsible for the results of this script, i make no promise to the safety of the resulting output.
