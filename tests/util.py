import os, csv
from matchco import subsequences


def generate_test_data(datafile):
   pth = os.sep.join((os.path.dirname(__file__), datafile))
   with open(pth) as csvfile:
      reader = csv.reader(csvfile, delimiter=';', quotechar='"')
      for name, tested in reader:
         name = name.strip()
         tested = tested.strip()
         if tested:
            name, tested = name.lower(), tested.lower()
            yield (name, tested.split(','))


def candidate_data(testdata):
   names = [tdi[0] for tdi in testdata]
   return [(n, n, subsequences(n)+[n]) for n in names]
