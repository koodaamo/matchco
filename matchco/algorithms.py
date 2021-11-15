# draft implementation of sift4 in Python:
# see http://siderite.blogspot.com/2014/11/super-fast-and-accurate-string-distance.html
# or https://web.archive.org/web/20150913164823/ + above URL

def sift4(s1, s2, maxOffset=9999):

   l1 = len(s1)
   l2 = len(s2)

   c1 = 0
   c2 = 0
   lcss = 0
   local_cs = 0

   while (c1 < l1) and (c2 < l2):
      if s1[c1] == s2[c2]:
         local_cs += 1
      else:
         lcss += local_cs
         local_cs = 0
         if c1 != c2:
            c1 = c2 = max(c1, c2)
            #using max to bypass the need for computer transpositions ('ab' vs 'ba')
         i=0
         while (i < maxOffset) and (((c1 + i) < l1) or ((c2 + i) < l2)):
            if (c1 + i < l1) and (s1[c1 + i] == s2[c2]):
               c1 += i
               local_cs += 1
               break
            if (c2 + i < l2) and s1[c1] == s2[c2 + i]:
               c2 += i
               local_cs +=1
               break
            i+=1
      c1+=1
      c2+=1
   lcss += local_cs
   return round(max(l1, l2) - lcss)
