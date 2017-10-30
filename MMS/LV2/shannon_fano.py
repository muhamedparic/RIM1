class ShannonFanoCoder:
    def __init__(self, text):
        self._freq_dict = {}
        for char in text:
            if not char in self._freq_dict:
                self._freq_dict[char] = 1
            else:
                self._freq_dict[char] += 1
        self._chars = []
        for char, freq in self._freq_dict.items():
            self._chars.append((char, freq, []))
        self._chars.sort(key=lambda x: x[1], reverse=True)
        self._run()

    #Returns the length of the first half
    @staticmethod
    def _split(chars):
        occur_sum = 0
        for char, freq, code in chars:
            occur_sum += freq
        first_half_occur_sum = chars[0][1]
        for i in range(1, len(chars)):
            second_half_occur_sum = occur_sum - first_half_occur_sum
            cur_diff = abs(first_half_occur_sum - second_half_occur_sum)
            if cur_diff < abs(first_half_occur_sum - second_half_occur_sum + 2 * chars[i][1]):
                return i
            else:
                first_half_occur_sum += chars[i][1]

    @staticmethod
    def _run_node(chars):
        if len(chars) == 1:
            return
        if len(chars) == 0:
            raise Exception('AAAAAAAA')
        first_half_len = ShannonFanoCoder._split(chars)
        for i in range(len(chars)):
            if i < first_half_len:
                chars[i][2].append(0)
            else:
                chars[i][2].append(1)
        ShannonFanoCoder._run_node(chars[:first_half_len])
        ShannonFanoCoder._run_node(chars[first_half_len:])

    def _run(self):
        ShannonFanoCoder._run_node(self._chars)
        return self

    @property
    def codes(self):
        return sorted([(char, code) for char, freq, code in self._chars], key=lambda x: len(x[1]))

    @property
    def occurances(self):
        return self._freq_dict

    @property
    def compression_ratio(self):
        uncompressed_size = 8 * sum((freq for char, freq, code in self._chars))
        compressed_size = sum((freq * len(code) for char, freq, code in self._chars))
        return uncompressed_size / compressed_size


def test(test_string):
    c = ShannonFanoCoder(test_string)
    print('String: ', test_string)
    for code in c.codes:
        print(code)
    print('Compression ratio: ', c.compression_ratio)
    print()

test(u'Algoritam Shannon - Fanovog kodiranja je jednostavan za implementirati.')
test(u'Da bi student mogao implementirati algoritam potrebno je da pročita predavanja iz predmeta MMS.')
test(u'Za svaku od ovih rečenica potrebno je izračunati stepen kompresije ako se za nekomprimirani \
tekst koristi bitna reprezentacija ASCII vrijednosti simbola.')
