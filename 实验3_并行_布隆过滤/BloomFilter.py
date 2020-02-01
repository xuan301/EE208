from Bitarray import Bitarray
import mmh3

class BloomFilter(set):
    def __init__(self,size,hash_num):
        super(BloomFilter,self).__init__()
        self.bitarray = Bitarray(size)
        self.size = size
        self.hash_num = hash_num

    def __len__(self):
        return self.size

    def __iter__(self):
        return iter(self.bitarray)

    def add(self,item):
        for i in range(self.hash_num):
            index = mmh3.hash(item,i) %self.size
            self.bitarray.set(index)

        return self

    def __contains__(self, item):
        flag = True
        for i in range(self.hash_num):
            index = mmh3.hash(item,i)%self.size
            if self.bitarray.get(index) == 0:
                flag = False

        return flag

if __name__ == '__main__':
    bloomfilter = BloomFilter(100,10)
    foods = ['fish','fries','jam','juice','jello','chocolate','sandwich','hamburger',
             'rice','coke','milk','tea','ham','egg','buscuit','toast','mean',
             'bun','potato','tomato','broccoli','celery','garlic','onion']

    for food in foods:
        bloomfilter.add(food)

    count = 0
    for food in foods:
        if food in bloomfilter:
            print('{} is in bloom filter as expected'.format(food))
        else:
            print('There is a false positive with {}'.format(food))
            count += 1

    tests = ['cowpea','cabbage','soybean','apple','pear','banana','peach',
             'watermelon','lemon','pineapple','yangtao','orange',
             'grapefruit','apricot','coconut','jujube','grape','meat','chicken']

    total = len(foods)+len(tests)
    for test in tests:
        if test in bloomfilter:
            print('There is a false positive with {} in test'.format(test))
            count += 1
        else:
            print('{} is not in the bloom filter as expected'.format(test))

    print("The false negative rate is {:.2%}".format(count/total))