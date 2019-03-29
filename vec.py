import struct
import numpy as np
import bisect

def scan_size(fp):
	s=b''
	c=b''
	while c!=b' ' and c!=b"\n":
		c=fp.read(1)
		s+=c
	return int(s)

def scan_word(fp):
	s=b''
	c=b''
	#while c!=b' ' and c!=b'\n':
	c=fp.read(1)
	if c!=b"\n":
		s+=c
	while c!=b' ':
		c=fp.read(1)
		s+=c
	return s

def load_word2vec(filename="vector.bin"):
	fp = open(filename, "rb")
	word_size=scan_size(fp)
	vec_size=scan_size(fp)

	print(word_size)
	print(vec_size)
	words=[]
	vectors=[]
	for i in range(word_size):
		w=scan_word(fp)
		vec=np.zeros((vec_size,))
		for j in range(vec_size):
			a=struct.unpack('f',fp.read(4))
			vec[j]=a[0]
		ww=""
		try:
			ww=w.decode(encoding='utf-8')
		except:
			continue
		words.append([ww,i])
		vectors.append(vec)
	vectors=np.array(vectors)
	#print("...start")

	sorted_words=sorted(words)
	words_x=[el[0] for el in sorted_words]
	words_index=[el[1] for el in sorted_words]

	return words,vectors,words_x,words_index

def find_vector_index(search_str,words_x,words_index):
	index1 = bisect.bisect_left(words_x, search_str)
	i1=words_index[index1]
	return i1

def nearest_words(vv,words,vectors,K=10):
	d=np.sum((vectors-vv)**2,axis=1)
	indices=np.argpartition(d,K)[:K]
	outputs=sorted([[d[i],words[i][0]] for i in indices])
	return outputs

"""
search_str="マドリード"
index2 = bisect.bisect_left(words_x, search_str)
print(index2)

search_str="イタリア"
index3 = bisect.bisect_left(words_x, search_str)
print(index3)
i1=words_index[index1]
i2=words_index[index2]
i3=words_index[index3]

v1=vectors[i1]
v2=vectors[i2]
v3=vectors[i3]
vv=v3+v2-v1

d=np.sum((vectors-vv)**2,axis=1)
aa=np.argmin(d)
print(aa)
K=10
indices=np.argpartition(d,K)[:K]
outputs=sorted([[d[i],words[i][0]] for i in indices])
for el in outputs:
	print(el[1],el[0])

  for (b = 0; b < words; b++) {
    a = 0;
    while (1) {
      vocab[b * max_w + a] = fgetc(f);
      if (feof(f) || (vocab[b * max_w + a] == ' ')) break;
      if ((a < max_w) && (vocab[b * max_w + a] != '\n')) a++;
    }
    vocab[b * max_w + a] = 0;
    for (a = 0; a < size; a++) fread(&M[a + b * size], sizeof(float), 1, f);
    len = 0;
    for (a = 0; a < size; a++) len += M[a + b * size] * M[a + b * size];
    len = sqrt(len);
    for (a = 0; a < size; a++) M[a + b * size] /= len;
  }
 
"""
