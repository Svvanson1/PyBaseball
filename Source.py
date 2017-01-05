#!/cygdrive/c/Python34/python
#!/usr/bin/python

from random import randrange
from random import uniform
from math import sqrt

#Note average runs per game (both teams) in 2014: 8.13
#     average batting average:                    0.253

#-------------- Subs --------------------#

# Return result given OBP (batting avg), SLG (slugging pct), OOBP (opponents on base pct)
def at_bat(OBP, SLG, OOBP):
    rand = uniform(0,1)
    extrabase_factor = (SLG)/OBP
    #hits (walk blened with short-single, SS)
    if rand < adj_OBP/(extrabase_factor**4):   return "TPL"
    if rand < adj_OBP/(extrabase_factor**3):   return "HR"
    if rand < adj_OBP/(extrabase_factor**2):   return "DB"
    if rand < adj_OBP/(extrabase_factor**1.5): return "LS"
    if rand < adj_OBP: return "SS"
    #outs (all sacrifices currently sac-fly (SF))
    if rand < adj_OBP*1.8: return "SF"
    if rand < adj_OBP*2.2: return "SO" #strike-out
    if rand < adj_OBP*2.4: return "FC" #fielders choice
    return "DP" #double-play ball

#Determine if at-bat code is a hit or not, return True if hit (or walk)
def is_hit(ab_code):
   if ab_code == "TPL": return True
   if ab_code == "HR":  return True
   if ab_code == "DB":  return True
   if ab_code == "LS":  return True
   if ab_code == "SS":  return True
   return False

#Determine if runners advance, 1 if true
def advances_runner(ab_code):
    if is_hit:          return True
    if ab_code == "SF": return True
    return False


class HalfInning:
    def __init__(self,is_top):
        self.is_top = is_top
        self.first  = False
        self.second = False
        self.third  = False
        self.outs   = 0
        self.runs   = 0
    def any_base_runners_q(self):
        return 1*(self.first or self.second or self.third)
    def advance_runners_by1(self):
        if self.third: 
             self.runs = self.runs + 1 #score a run
             self.third  = False
        if self.second:
             self.third  = True
             self.second = False
        if self.first:
             self.second = True
             self.first  = False
    def double(self):
       self.runs = self.runs + 1*self.third + 1*self.second
       self.third = self.first; self.first  = False 
       self.second = True # batter becomes runner
    def tripple(self):
       self.runs = runs + 1*self.third + 1*self.second + 1*self.first
       self.second = self.first = False
       self.third = True # batter becomes runner 
    def home_run(self):
       self.runs = runs + 1*self.third + 1*self.second + 1*self.first + 1
       self.first = self.second = self.third = False  # clear all bases
    def double_play_ball(self):
       if self.any_base_runners_q(): 
           self.outs = self.outs + 2
           if self.third:
              self.third = False
           elif self.second:
              self.second = False
           else: self.first = False
       else:
           self.outs = self.outs + 1
    def short_single(self):
        self.advance_runners_by1()
        self.first = True

    def out_no_advance(self):
        self.outs = self.outs + 1
              
    def done(self):
       return self.outs >= 3
 
    def runs_scored(self):
       return self.runs

 
#============= END Subs =================#

print("Play Ball!")
adj_OBP = input("Enter the batting average for this batter: ")

runs_vis = runs_home = 0  # Runs for each team, vistors, home

x = 1
top = True
while (x <= 17) or ((x == 18) and (runs_vis >= runs_home)):
    top = ((x % 2) == 1)
    hinn = HalfInning(top)
    if top:  
       print("\n=================================")
       print("  Top of Inning: " + str(int(x/2+0.5))) 
    else: 
       print("  Bottom of Inning: " + str(int(x/2+0.5)))

    while(not hinn.done()):
       ab_result = at_bat(0.481,0.500,0.253)
       hit = is_hit(ab_result) 

       if ab_result == "DB": 
          hinn.double_play_ball()
       elif hit:
          hinn.short_single()
       else :   hinn.out_no_advance()

    if top:
       runs_vis  += hinn.runs_scored()
    else:
       runs_home += hinn.runs_scored()
    
    print("  Score-> Visitors: " + str(runs_vis) + " Home: " + str(runs_home))
    
    x += 1
