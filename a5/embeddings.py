
import math
import numpy as np
import pandas as pd
class Embeddings:

    def __init__(self, glove_file = '/projects/e31408/data/a5/glove_top50k_50d.txt'):
        self.embeddings = {}
        self.word_rank = {}
        for idx, line in enumerate(open(glove_file)):
            row = line.split()
            word = row[0]
            vals = np.array([float(x) for x in row[1:]])
            self.embeddings[word] = vals
            self.word_rank[word] = idx + 1

    def __getitem__(self, word):
        return self.embeddings[word]

    def __contains__(self, word):
        return word in self.embeddings

    def vector_norm(self, vec):
        """
        Calculate the vector norm (aka length) of a vector.

        This is given in SLP Ch. 6, equation 6.8. For more information:
        https://en.wikipedia.org/wiki/Norm_(mathematics)#Euclidean_norm

        Parameters
        ----------
        vec : np.array
            An embedding vector.

        Returns
        -------
        float
            The length (L2 norm, Euclidean norm) of the input vector.
        """
        norm_sum = 0
        for element in vec:
            try:
                norm_sum += element**2
            except:
                val = 3
                #print("this is norm sum "+ str(norm_sum))
                #print("this is element " + str(element))
        # >>> YOUR ANSWER HERE
        return math.sqrt(norm_sum)
        # >>> END YOUR ANSWER

    def dot_prod(self,vec1,vec2):
        prod_sum = 0
        if isinstance(vec2[0],str):
            vec2 = vec2[1]
        for i in range(len(vec1)):
            #print("doing "+ str(vec1[i])+" times "+ str(vec2[i]))
            try:
                prod_sum += vec1[i] * vec2[i]
            except:
                print("i is "+str(i))
                print("this is vector 1"+str(vec1))
                print("this is vector 2"+str(vec2))
        return prod_sum
    def cosine_similarity(self,vector1,v2):
        """
        Calculate cosine similarity between v1 and v2; these could be
        either words or numpy vectors.

        If either or both are words (e.g., type(v#) == str), replace them 
        with their corresponding numpy vectors before calculating similarity.

        Parameters
        ----------
        v1, v2 : str or np.array
            The words or vectors for which to calculate similarity.

        Returns
        -------
        float
            The cosine similarity between v1 and v2.
        """
        
        if isinstance(vector1,str):
            vector1 = self.embeddings[vector1]
            #print("we got one!")
        if isinstance(v2,str):
            vnew = self.embeddings[v2]
            v2 = self.embeddings[v2]
        #print("this is vector 1 stuff" + str(vector1))
        #print("this vector 2 stuff" + str(v2[1]))
        dot_prod = self.dot_prod(vector1,v2)
        #print(v2[1])
        #if type(v2) == np.float64:
        #    v2 = [v2]
        #if type(vector1) == np.float64:
           # vector1 = [vector1]
        try:
            cos_sim = dot_prod/(self.vector_norm(vector1) * self.vector_norm(v2))
        except:
            cos_sim = dot_prod/(self.vector_norm(vector1) * self.vector_norm(v2[1]))
        #print("this is cos_sim" +str(cos_sim))
        return cos_sim
        # >>> END YOUR ANSWER
    
    def most_similar(self, vec, n = 5, exclude = []):
        """
        Return the most similar words to `vec` and their similarities. 
        As in the cosine similarity function, allow words or embeddings as input.


        Parameters
        ----------
        vec : str or np.array
            Input to calculate similarity against.

        n : int
            Number of results to return. Defaults to 5.

        exclude : list of str
            Do not include any words in this list in what you return.


        Returns
        -------
        list of ('word', similarity_score) tuples
            The top n results.        
        """
        if type(vec) == str:
            vectah = self.embeddings[vec]
        else:
            vectah = vec
        this_shit = np.array(list(self.embeddings.items()))
        cos_arr = np.zeros([2,len(this_shit)])
        word_list = [0]* n
        val_list = [0] * n
        count = 0  
        for key in this_shit:
            if key[0] not  in exclude:
                
                tup = (key[0], self.cosine_similarity(vectah,key))
                #word_list.append(key[0])
                #val_list.append(self.cosine_similarity(vectah,key))
                thing = self.cosine_similarity(vectah,key)
                startpos = n
                for i in range(0,n):
                    where =(i-(n-1))*-1
                    #print(where)
                    if thing > val_list[where]:
                        #startpos = where
                        startpos -= 1
                    else:
                        break
                    
                val_list.insert(startpos,thing)
                word_list.insert(startpos,key[0])
            count += 1
            
        top_list = [0.0]*len(word_list)
        for exword in word_list:
            try:
                if exword in exclude:
                    ind = word_list.index(exword)
                    word_list.pop(ind)
                    val_list.pop(ind)
            except:
                yuh = 2
                #print(exword)
        #for i in range(len(word_list)):
            #if i % 100 == 0:
            #    print("We are " +str(i/len(word_list))+ "through this shit")
            #pointer = 0
            #done = False
            #while done == False:
            #    if val_list[i]>top_list[pointer]:
            #        done = False
            #    else:
            #        done = True
            #    if pointer == len(top_list)-1 :
            #        done = True
            #    pointer =+ 1
            #top_list[pointer - 1] = i
        
        
        #chopped_cos_arr = cos_list[0:n]
        embeds = []
        for i in range(n):
            latest = (word_list[i],val_list[i])
            embeds.append(latest)
        #chopped_cos_arr = [(word_list[0],val_list[0]),(word_list[1],val_list[1]),(word_list[2],val_list[2]),(word_list[3],val_list[3]),(word_list[4],val_list[4])]
        
                           
        # >>> YOUR ANSWER HERE
        #print(val_list[0:10])
        #print(chopped_cos_arr)
        return embeds
        # >>> END YOUR ANSWER

if __name__ == '__main__':
    embeddings = Embeddings()
    word = 'bitch'
    print(f'Most similar to {word}:')
    #print(embeddings.most_similar(word,5))
    for item in embeddings.most_similar(word,10, exclude=[word]):
        try:
            print('\t',item[0], '\t', item[1])
        except:
            print("FUCK")
            #print(item)


