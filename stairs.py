import math
import csv
import os
import matplotlib.pyplot as plt

# THESE PARAMATERS CAN BE CHANGED
top_landing_overhang = 20
post_width = 40
stringer_width = 40
stringer_depth = 80
tread_thickness = 40
tread_depth = 280
handrail_width = 30
handrail_height = 910
handrail_gap = 70
step_protrusion = 40

class Stairs(object):

    """ The stairs class, this is just a basic straight flight of stairs """

    def __init__(self, name):
        self.name = name
        self.going = 250
        self.rise = None
        self.ri_max = 220
        self.ri_min = 150
        self.going_min = 220
        self.pitch = None
        self.width = 1000
        self.trs = None
        self.height = 3000
        self.travel_max = 4020
        self.travel = None
        self.tworplusg = None
        self.hratio = None
        self.vratio = None
        self.htov = None # convert horizontal distances to verticle
        self.vtoh = None #convert vertical distances to horizontal
        self.trtostrv = None # Vertical distance from front edge of thread to top of stringer
        # The distance the top landing overhangs the stairs
        self.overhang = top_landing_overhang
        # Size of posts, stringer and threads
        self.pw = post_width
        self.sw = stringer_width
        self.sd = stringer_depth
        self.trt = tread_thickness
        self.trd = tread_depth
        self.hrw = handrail_width
        self.hrh = handrail_height
        self.hrg = handrail_gap
        self.steppr = step_protrusion

    def input_data(self, height, travel_max, width, going, overhang):
        self.height = int(height)
        self.travel_max = int(travel_max)
        self.width = int(width)
        self.going = int(going)
        self.overhang = int(overhang)

    def calculate(self):
        # calculate the staircase paramaters
        self.trs = int((self.travel_max-self.overhang)/self.going)
        self.rise = self.height/(1.0+self.trs)
        self.pitch = math.degrees(
            math.atan(self.height/(self.trs*self.going+float(self.going))))
        self.hratio = 1/(math.cos(math.radians(self.pitch)))
        self.vratio = 1/(math.sin(math.radians(self.pitch)))
        self.htov = math.tan(math.radians(self.pitch))
        self.vtoh = 1/(math.tan(math.radians(self.pitch)))
        self.travel = self.trs*self.going+self.overhang
        self.htov = self.hratio/self.vratio
        self.trtostrv = (self.trd/2-(self.sd/2.0)*self.vratio)*self.htov + self.trt/2
        self.tworplusg = 2*self.rise + self.going
        self.store_warnings()

    def store_data(self):
        # Store the data in a list for printing or for displaying in kivy
        self.write_data = [self.name,
                           "Threads               "+str(self.trs),
                           "Pitch                 "+str(round(self.pitch, 2)),
                           "Proj. Dec.  "+"H: "+str(round(self.hratio, 4))+" , V: "+str(round(self.vratio,4)),
                           "Rise                  "+str(round(self.rise, 1)),
                           "Going                 "+str(self.going),
                           "Overhang              "+str(self.overhang),
                           "Travel                "+str(self.travel),
                           "Height                "+str(self.height),
                           "Width                 "+str(self.width),
                           "2R+G (Optimum 600)    "+str(int(self.tworplusg))]

    def store_warnings(self):
        # Store some warnings
        self.warnings = []
        if self.rise > self.ri_max:
            self.warnings.append("WARNING!: " +
                                 str(self.rise) +
                                 " rise is greater than the regulation max of " +
                                 str(self.ri_max) +
                                 ". Consider a longer travel or a shorter going")
        if self.going < self.going_min:
            self.warnings.append("WARNING!: " +
                                 str(self.going) +
                                 " going is less than the regulation min 220")
        if self.rise < self.ri_min:
            self.warnings.append("WARNING!: " +
                                 str(self.rise) +
                                 " rise is less than the regulation min 150")
        if self.pitch > 43.0:
            self.warnings.append("WARNING!: " +
                                 str(self.pitch) +
                                 " pitch is too steep. Regulation 42. Consider a longer travel")
        elif self.pitch > 42.0:
            self.warnings.append("WARNING!: " +
                                 str(self.pitch) +
                                 " is outside regulation of 42, but probably ok")
        if 500 > self.tworplusg or self.tworplusg > 700:
            self.warnings.append(
                "WARNING!: 2R+G = " + str(2 * self.rise + self.going) +
                "is outside regulation window of 500-700")

    def scale_draw(self):
        #Make a scale drawing of the threads with the stairs info on it.
        self.elfig = plt.figure(figsize=(10, 10))
        plt.minorticks_on()
        self.ax = plt.subplot(111)
        self.rect = self.elfig.patch  # used to add a white background.Only for plt.show()
        self.rect.set_facecolor((1, 1, 1))
        # Elevation
        self.ax.plot([-250, self.overhang], [self.height, self.height], linewidth=1.5, color='0.0')
        self.ax.plot([0, self.travel+500], [0, 0], linewidth=1.5, color=(0, 0, 0))
        self.ax.plot([0, 0], [0, self.height], linewidth=1.5, color=(0, 0, 0))
        x = 0
        y = self.height-self.rise
        for i in range(0, self.trs):
            self.ax.plot([x, x+self.going+self.overhang], [y, y], linewidth=1.5, color=(1, 0, 0))
            y += -self.rise
            x += self.going
        # Plan
        self.ax.plot([0, 0], [-self.width-100, -100], linewidth=1.5, linestyle='--', color='0.0')
        self.ax.plot([self.overhang, self.overhang],
                     [-self.width-100, -100], linewidth=1.5, color='0.0')
        self.ax.plot([0, self.travel],
                     [-self.width -100, - self.width -100], linewidth=1.5, color='0')
        self.ax.plot([0, self.travel], [-100, -100], linewidth=1.5, color=(0, 0, 0))
        self.ax.plot([0, self.travel], [-self.width-60,-self.width-60], linewidth=1.5, color='0.2')
        self.ax.plot([0, self.travel], [-140, -140], linewidth=1.5, color='0.2')
        x = self.overhang+self.going
        for i in range(0, self.trs):
            self.ax.plot([x, x], [-self.width-60, -140], linewidth=1.5, color=(1, 0, 0))
            x += self.going
        self.ax.grid(True, 'major', linestyle="-", axis='y', color='0.65')
        self.ax.grid(True, 'major', linestyle="-", axis='x', color='0.65')
        self.ax.grid(True, 'minor', linestyle="--", axis='y', color='0.75')
        self.ax.grid(True, 'minor', linestyle="--", axis='x', color='0.75')
        self.ax.axis('equal')
        self.ax.set_ylim(-self.width-200, self.height+100)
        y = 0.98
        for entry in self.write_data:
            self.ax.text(0.65, y, entry,
                         horizontalalignment='left',
                         verticalalignment='center',
                         backgroundcolor='1.0',
                         size=14,
                         transform=self.ax.transAxes)
            y += -0.03
        plt.tight_layout()  # handy for fixing borders etc.
        plt.savefig(os.path.join('output',self.name+'_drawing.png'), dpi=100)
        plt.show()

    def list_parts(self):
        cleat = self.going*self.hratio
        cleat_distances = [11,"Cleat distances"]
        distance = cleat
        for i in range(0,self.trs-1):
            cleat_distances.append(int(round(distance)))
            distance += cleat
        self.parts = [[self.name],
            ["GENERAL ATTRIBUTES"],
            ["Threads ",self.trs],
            ["Pitch ",round(self.pitch, 2)],
            ["Rise ",round(self.rise, 1)],
            ["Going ",self.going],
            ["Travel ", self.travel],
            ["Height ", self.height],
            ["Width ", self.width],
            ["Proj. Dec. H and V ",round(self.hratio,4),round(self.vratio,4)],
            ["Overhang ",self.overhang],
            ["2R+G ", int(self.tworplusg)],
            ["MESUREMENTS"],
            [1, "stringer length", int(round(self.hratio*(self.travel-self.pw-self.steppr)))],
            ["1A", "stringer plan length", self.travel-self.pw-self.steppr],
            [2, "handrail length", int(round(self.hratio*(self.travel-2*self.pw-self.steppr)))],
            [3, "bottom post length", int(round(self.rise-3+self.hrh+(self.steppr+self.pw)*(self.htov)))],
            [4, "top post length", int(round(self.trtostrv+(self.pw-self.overhang)*(self.htov)+1110))],
            [5, "spindel length", int(round(self.trtostrv+self.hrh-(self.hrg+2*self.hrw)*self.hratio))],
            [6, "string to bottom rail", int(round((self.trtostrv+self.hrh-(self.hrg+2*self.hrw)*self.hratio)/self.hratio))],
            [7, "nick to string", int(round(self.trtostrv-self.overhang*self.htov))],
            ["7A", "nick to cleat top", int(round(self.rise+self.trt))],
            [8, "bottom cleat height", int(round(self.rise-3-self.trt))],
            [9, "base plate to string", int(round(self.rise-3-self.trtostrv+(self.steppr+self.pw)*(self.htov)-self.sd*self.hratio))],
            [10, "cleat to string", int(round((225/2.0-(self.sd/2.0)*self.vratio-(self.trt/2.0)*self.vtoh)/self.vratio))],
            cleat_distances,
            ["PARTS"],
            ["Threads # w d t", self.trs,self.width-2*self.sw-3,self.trd,self.trt],
            ["Safety Bars # l", self.trs-1, self.width-self.sw],
            ["Braces # l", 3, self.width-2*self.sw],
                      ["Cleats #", 2*self.trs]]
        cs = csv.writer(open(os.path.join("output", self.name+'_parts.csv'), "w"))
        for row in self.parts:
            cs.writerow(row)


class CornerStairs(Stairs):

    """Corner stairs, fits a stairs with one turn within the given dimensions"""

    def __init__(self, name):
        Stairs.__init__(self, name)
        #Same paramaters as normal stairs plus some more
        self.boundary1 = None
        self.boundary1_max = None
        self.boundary2 = None
        self.travel1 = None
        self.travel2 = None
        self.fl1_threads = None
        self.fl2_threads = None
        self.overlap = None
        self.landing_protrusion = 10 # protrusion of landing past width of top flight
        self.landing_height = None
        self.tunr_direction = 'L'

    def input_data(self, height, boundary1_max, boundary2, width, going, overhang, turn):
        # travel_max now refers to boundary1_max
        self.height = int(height)
        self.boundary1_max = int(boundary1_max)
        self.boundary2 = int(boundary2)
        self.width = int(width)
        self.going = int(going)
        self.turn = turn

    def calculate(self):
        self.fl2_threads = int(math.ceil(
            (self.boundary2 - self.overhang - self.width + self.pw)/float(self.going)))
        self.overlap = self.fl2_threads*self.going+self.overhang-(self.boundary2-self.width + self.pw)
        # Maximum travel if the stairs were straight and the landing was a normal steps
        self.travel_max = ((self.fl2_threads+1)*self.going+self.overhang
                           +self.boundary1_max-self.width - self.landing_protrusion)
        Stairs.calculate(self)
        self.fl1_threads = self.trs-self.fl2_threads-1
        self.travel1 = self.fl1_threads*self.going+self.landing_protrusion
        self.travel2 = self.fl2_threads*self.going+self.overhang
        self.boundary1 = self.travel1+self.width
        self.landing_height = (self.fl1_threads+1)*self.rise
        self.store_data()
        self.store_warnings()

    def store_data(self):
        # Store the data in a list for printing or for displaying in kivy
        self.write_data = [self.name,
                           "Threads             " + str(self.trs) + "(" +str(self.fl1_threads) + "," + str(self.fl2_threads) + ")",
                           "Pitch                 " +str(round(self.pitch, 1)),
                           "Proj. Dec.          "+"H: "+str(round(self.hratio, 4))+" , V: "+str(round(self.vratio,4)),
                           "Rise                  " + str(round(self.rise, 1)),
                           "Going                 " + str(self.going),
                           "Overhang              "+str(self.overhang),
                           "Travels               " +str(self.travel1) + "," + str(self.travel2),
                           "Height                " + str(self.height) +"(" + str(int(round(self.landing_height))) + ")",
                           "Width                 " +str(self.width),
                           "Overlap               " + str(round(self.overlap)),
                           "Boundaries            " + str(self.boundary1) + "," + str(self.boundary2),
                           "2R+G (Optimum 600)    " + str(int(self.rise * 2 + self.going))]

    def store_warnings(self):
        # Store some warnings
        Stairs.store_warnings(self)
        if self.overlap > 180:
            self.warnings.append("WARNING!: " + str(self.overlap) +
                                 " overlap is quiet large")
            self.warnings.append("Consider a different width or going")

    def scale_draw(self):
        #Make a scale drawing of the threads with the stairs info on it.
        self.elfig = plt.figure(figsize=(10, 10))
        plt.minorticks_on()
        self.ax = plt.subplot(111)
        self.rect = self.elfig.patch  # used to add a white background.Only for plt.show()
        self.rect.set_facecolor((1, 1, 1))
        # Elevation
        self.ax.plot([-250, self.overhang], [self.height, self.height], linewidth=1.5, color='0.0')
        self.ax.plot([0, 0], [0, self.height], linewidth=1.5, color='0')
        self.ax.plot([0, self.boundary2], [0, 0], linewidth=1.5, color='0')
        self.ax.plot([self.boundary2, self.boundary2], [0, self.height+100], linewidth=1.5, color='0')
        x = 0
        y = self.height-self.rise
        # Top flight
        for i in range(0, self.fl2_threads):
            self.ax.plot([x, x+self.going+self.overhang], [y, y], linewidth=1.5, color=(1,0,0))
            y += -self.rise
            x += self.going
        #Landing
        self.ax.plot([self.boundary2-self.width+40, self.boundary2],
                     [self.landing_height, self.landing_height], linewidth=1.5, color=(1,0,0))
        #Bottom flight
        y += -self.rise
        for i in range(0, self.fl1_threads):
            self.ax.plot([self.boundary2-self.width+40, self.boundary2-40],
                         [y, y], linewidth=1.5, color=(1,0,0))
            y += -self.rise

        self.ax.grid(True, 'major', linestyle="-", axis='y', color='0.65')
        self.ax.grid(True, 'major', linestyle="-", axis='x', color='0.65')
        self.ax.grid(True, 'minor', linestyle="--", axis='y', color='0.75')
        self.ax.grid(True, 'minor', linestyle="--", axis='x', color='0.75')
        self.graphspan = 0
        if self.boundary1 > self.height:
            self.graphspan = self.boundary1+200
        else:
            self.graphspan = self.height +200
        self.ax.axis('equal')
        self.ax.set_ylim(-200, self.graphspan)
        self.ax.set_xlim(-200, self.graphspan)
        y = 0.98
        for entry in self.write_data:
            self.ax.text(0.65, y, entry,
                         horizontalalignment='left',
                         verticalalignment='center',
                         backgroundcolor='1.0',
                         size=14,
                         transform=self.ax.transAxes)
            y += -0.03
        plt.tight_layout()  # handy for fixing borders etc.
        plt.savefig(os.path.join('output',self.name+'_elevation'+'.png'), dpi=100)
        # PLAN
        self.pfig = plt.figure(figsize=(10, 10))
        plt.minorticks_on()
        self.pax = plt.subplot(111)
        self.rect = self.pfig.patch  # used to add a white background.Only for plt.show()
        self.rect.set_facecolor((1, 1, 1))
        #Walls
        self.pax.plot([-150, self.boundary2],[0, 0], linewidth=1.5, color='0')
        self.pax.plot([0, 0],[self.width, self.width+200], linewidth=1.5, color='0')
        self.pax.plot([self.boundary2, self.boundary2],
                      [0, self.boundary1+200], linewidth=1.5, color='0')
        self.pax.plot([0, 0], [0,self.width], linewidth=1.5, linestyle='--', color='0.0')
        #Top Flight
        self.pax.plot([self.overhang, self.overhang],
                     [0, self.width], linewidth=1.5, color='0.0')
        self.pax.plot([0, self.boundary2-self.width+40],[40, 40], linewidth=1.5, color='0.2')
        self.pax.plot([0, self.boundary2-self.width+40],
                     [self.width-40, self.width-40], linewidth=1.5, color='0.2')
        self.pax.plot([0, self.boundary2-self.width+40],
                     [self.width, self.width], linewidth=1.5, color='0.0')
        x = self.overhang+self.going
        for i in range(0, self.fl2_threads):
            self.pax.plot([x, x], [40, self.width-40], linewidth=1.5, color=(1, 0, 0))
            x += self.going
        self.pax.plot([self.boundary2+self.overlap+40-self.width, self.boundary2-self.width+40],
                      [40, 40], linewidth=1.5, color=(1, 0, 0))
        self.pax.plot([self.boundary2+self.overlap+40-self.width, self.boundary2-self.width+40],
                      [self.width-40, self.width-40], linewidth=1.5, color=(1, 0, 0))
        # Landing
        self.pax.plot([self.boundary2-self.width+40, self.boundary2-self.width+40],
                     [0, self.width+self.landing_protrusion], linewidth=1.5, linestyle='--', color=(1,0,0))
        self.pax.plot([self.boundary2-self.width+40, self.boundary2],
                     [self.width+self.landing_protrusion, self.width+self.landing_protrusion],
                      linewidth=1.5, color=(1,0,0))
        #Lower Flight
        self.pax.plot([self.boundary2-self.width+40, self.boundary2-self.width+40],
                     [self.width, self.boundary1], linewidth=1.5, color='0.2')
        self.pax.plot([self.boundary2-40, self.boundary2-40],
                     [self.width, self.boundary1], linewidth=1.5, color='0.2')
        self.pax.plot([self.boundary2-self.width, self.boundary2-self.width],
                     [self.width, self.boundary1], linewidth=1.5, color='0.0')

        y = self.width+self.going+self.landing_protrusion
        for i in range(0, self.fl1_threads):
            self.pax.plot([self.boundary2-self.width+40, self.boundary2-40],
                          [y, y], linewidth=1.5, color=(1, 0, 0))
            y += self.going

        self.pax.grid(True, 'major', linestyle="-", axis='y', color='0.65')
        self.pax.grid(True, 'major', linestyle="-", axis='x', color='0.65')
        self.pax.grid(True, 'minor', linestyle="--", axis='y', color='0.75')
        self.pax.grid(True, 'minor', linestyle="--", axis='x', color='0.75')
        self.pax.axis('equal')
        self.graphspan = 0
        if self.boundary1 > self.boundary2+200:
            self.graphspan = self.boundary1+200
        else:
            self.graphspan = self.boundary2 +200
        self.pax.axis('equal')
        self.pax.set_ylim(-200, self.graphspan)
        if self.turn == 'L':
            self.pax.set_ylim(self.graphspan, -200)

        self.pax.set_xlim(-200, self.graphspan)
        plt.tight_layout()  # handy for fixing borders etc.
        plt.savefig(os.path.join('output',self.name+'_plan.png'), dpi=100)
        plt.show()

    def list_parts(self):
        cleat = self.going*self.hratio
        cleat_distances = [4,"Cleat distances"]
        distance = cleat
        number = self.fl1_threads
        if self.fl2_threads > self.fl1_threads:
            number = self.fl2_threads
        for i in range(0,number-1):
            cleat_distances.append(int(round(distance)))
            distance += cleat
        self.parts = [[self.name],
            ["GENERAL ATTRIBUTES"],
            ["Pitch ",round(self.pitch, 2)],
            ["Rise ",round(self.rise, 1)],
            ["Going ",self.going],
            ["Height ", self.height],
            ["Width ", self.width],
            ["Threads Tot F1 F2", self.trs, self.fl1_threads, self.fl2_threads],
            ["Travels F1 F2", self.travel1, self.travel2],
            ["Landing height", int(round(self.landing_height))],
            ["Overlap landing", self.overlap],
            ["Proj. Dec. H and V ",round(self.hratio,4),round(self.vratio,4)],
            ["Overhang top",self.overhang],
            ["Width ", self.width],
            ["2R+G ", int(self.tworplusg)],
            ["MESUREMENTS"],
            ["FLIGHT #1"],
            [1, "stringer length", int(round(self.hratio*(self.travel1-self.pw-self.steppr-5)))],
            ["1A", "stringer plan length", self.travel1-self.pw-self.steppr-5],
            [2, "handrail length", int(round(self.hratio*(self.travel1-self.pw-self.steppr-5)))],
            [3, "bottom post length", int(round(self.rise-3+self.hrh+(self.steppr+self.pw)*(self.htov)))],
            [4, "nick to string", int(round(self.trtostrv-(self.landing_protrusion-5)*self.htov))],
            ["4A", "nick to cleat top", int(round(self.rise+self.trt))],
            [5, "bottom cleat height", int(round(self.rise-3-self.trt))],
            [6, "base plate to string", int(round(self.rise-3-self.trtostrv+(self.steppr+self.pw)*(self.htov)-self.sd*self.hratio))],
            ["FLIGHT #2"],
            [1, "stringer length", int(round(self.hratio*(self.travel2-self.pw-self.overlap)))],
            ["1A", "stringer plan length", self.travel2-self.pw-self.overlap],
            [2, "handrail length", int(round(self.hratio*(self.travel2-2*self.pw-self.overlap)))],
            [3, "Corner post length", int(round(self.rise+self.hrh+(self.overlap+self.pw)*self.htov+self.trtostrv+self.sd*self.hratio-(self.landing_protrusion-5)*self.htov+10))],
            [4, "top post length", int(round(self.trtostrv+(self.pw-self.overhang)*(self.htov)+1110))],
            [5, "Landing to sringer", int(round(self.rise-self.trtostrv+(self.overlap+self.pw)*(self.htov)-self.sd*self.hratio))],
            [6, "Bottom of post to landing", int(round(self.trtostrv+self.sd*self.hratio+10-(self.landing_protrusion-5)*self.htov))],
            [7, "bottom cleat to landing", int(round(self.rise-self.trt))],
            [8, "bottom of post to stringer", int(round(self.rise+(self.overlap+self.pw)*self.htov+10-(self.landing_protrusion-5)*self.htov))],
            [9, "nick to string", int(round(self.trtostrv-self.overhang*self.htov))],
            ["9A", "nick to cleat top", int(round(self.rise+self.trt))],
            ["BOTH"],
            [1, "spindel length", int(round(self.trtostrv+self.hrh-(self.hrg+2*self.hrw)*self.hratio))],
            [2, "string to bottom rail", int(round((self.trtostrv+self.hrh-(self.hrg+2*self.hrw)*self.hratio)/self.hratio))],
            [3, "cleat to string", int(round((225/2.0-(self.sd/2.0)*self.vratio-(self.trt/2.0)*self.vtoh)/self.vratio))],
            cleat_distances,
            ["PARTS"],
            ["Threads #, w, d, t", self.trs,self.width-2*self.sw-3,self.trd,self.trt],
            ["Safety Bars #, l", self.trs-1, self.width-self.sw],
            ["Braces #, l", 3, self.width-2*self.sw],
            ["Cleats #", 2*self.trs]]
        cs = csv.writer(open(os.path.join("output", self.name+'_parts.csv'), "w"))
        for row in self.parts:
            cs.writerow(row)


class TwoCornerStairs(CornerStairs):

    """The two corner fit a stairs with two turns within the given dimensions"""

    def __init__(self, name):
        CornerStairs.__init__(self, name)
        #Same paramaters as normal stairs plus some more
        self.boundary3 = None
        self.travel3 = None
        self.fl3_threads = None
        self.overlap2 = None
        self.landing_height2 = None

    def input_data(self, height, boundary1_max, boundary2, boundary3, width, going, overhang, turn):
        # travel_max now refers to boundary1_max
        self.height = int(height)
        self.boundary1_max = int(boundary1_max)
        self.boundary2 = int(boundary2)
        self.boundary3 = int(boundary3)
        self.width = int(width)
        self.going = int(going)
        self.turn = turn

    def calculate(self):
        self.fl3_threads = int(math.ceil(( # Round up the division
            self.boundary3 - self.overhang - self.width + self.pw)/float(self.going)))
        self.overlap2 = self.fl3_threads*self.going+self.overhang-(self.boundary3-self.width + self.pw)
        self.fl2_threads = int(math.ceil(( # Round up the division
            self.boundary2 - self.landing_protrusion - self.width*2 + self.pw)/float(self.going)))
        self.overlap = self.fl2_threads*self.going+self.landing_protrusion-(self.boundary2-2*self.width + self.pw)
        # Maximum travel if the stairs were straight and the two landing were a normal steps
        self.travel_max = ((self.fl3_threads+self.fl2_threads+2)*self.going+self.overhang
                           +self.boundary1_max-self.width-self.landing_protrusion)
        # calculate the staircase paramaters by treating stairs as straight
        Stairs.calculate(self)
        self.fl1_threads = self.trs-self.fl2_threads-self.fl3_threads - 2
        self.travel1 = self.fl1_threads*self.going+self.landing_protrusion
        self.travel2 = self.fl2_threads*self.going+self.landing_protrusion
        self.travel3 = self.fl3_threads*self.going+self.overhang
        self.boundary1 = self.travel1+self.width
        self.landing_height = (self.fl1_threads+1)*self.rise
        self.landing_height2 = (self.fl1_threads+self.fl2_threads+2)*self.rise
        self.store_data()
        self.store_warnings()

    def store_data(self):
        # Store the data in a list for printing or for displaying in kivy
        self.write_data = [self.name,
                           ("Threads              " + str(self.trs) + "(" +str(self.fl1_threads)
                            + "," + str(self.fl2_threads)+','+str(self.fl3_threads) + ")"),
                           "Pitch                 " +str(round(self.pitch, 2)),
                           "Proj. Dec.          "+"H: "+str(round(self.hratio, 4))+" , V: "+str(round(self.vratio,4)),
                           "Rise                  " + str(round(self.rise, 1)),
                           "Going                 " + str(self.going),
                           "Overhang              "+str(self.overhang),
                           "Travels               " +str(self.travel1) + "," + str(self.travel2),
                           ("Height                " + str(self.height) +"(" +
                            str(int(round(self.landing_height)))+","+str(int(round(self.landing_height2)))+ ")"),
                           "Width                 " +str(self.width),
                           ("Overlaps               " +
                            str(round(self.overlap)) + ','+str(round(self.overlap2))),
                           ("Boundaries(1,2,3)         " + str(self.boundary1) + ","
                            + str(self.boundary2) + ','+ str(self.boundary3)),
                           "2R+G (Optimum 600)    " + str(int(self.rise * 2 + self.going))]

    def store_warnings(self):
        # Store some warnings
        Stairs.store_warnings(self)
        if self.overlap > 180:
            self.warnings.append("WARNING!: " + str(self.overlap) +
                                 " overlap is quiet large")
            self.warnings.append("Consider a different width or going")

    def scale_draw(self):
        #Make a scale drawing of the threads with the stairs info on it.
        self.elfig = plt.figure(figsize=(10, 10))
        plt.minorticks_on()
        self.ax = plt.subplot(111)
        self.rect = self.elfig.patch  # used to add a white background.Only for plt.show()
        self.rect.set_facecolor((1, 1, 1))
        # Elevation
        #Walls
        self.ax.plot([-250, self.overhang], [self.height, self.height], linewidth=1.5, color='0.0')
        self.ax.plot([0, 0], [0, self.height], linewidth=1.5, color='0')
        self.ax.plot([0, self.boundary3], [0, 0], linewidth=1.5, color='0')
        self.ax.plot([self.boundary3, self.boundary3], [0, self.height+100], linewidth=1.5, color='0')
        # Top flight
        x = 0
        y = self.height-self.rise
        for i in range(0, self.fl3_threads):
            self.ax.plot([x, x+self.going+self.overhang], [y, y], linewidth=1.5, color=(1,0,0))
            y += -self.rise
            x += self.going
        #Top Landing
        self.ax.plot([self.boundary3-self.width+40, self.boundary3],
                     [self.landing_height2, self.landing_height2], linewidth=1.5, color=(1,0,0))
        #Middle flight
        y += -self.rise
        for i in range(0, self.fl2_threads):
            self.ax.plot([self.boundary3-self.width+40, self.boundary3-40],
                         [y, y], linewidth=1.5, color=(1,0,0))
            y += -self.rise
        #Bottom Landing
        self.ax.plot([self.boundary3-self.width-10, self.boundary3],
                     [self.landing_height, self.landing_height], linewidth=1.5, color=(1,0,0))
        #Bottom Flight
        x = self.boundary3-self.width-10-self.going
        y += -self.rise
        for i in range(0, self.fl1_threads):
            self.ax.plot([x, x+self.going+self.overhang], [y, y], linewidth=1.5, color=(1,0,0))
            y += -self.rise
            x -= self.going

        self.ax.grid(True, 'major', linestyle="-", axis='y', color='0.65')
        self.ax.grid(True, 'major', linestyle="-", axis='x', color='0.65')
        self.ax.grid(True, 'minor', linestyle="--", axis='y', color='0.75')
        self.ax.grid(True, 'minor', linestyle="--", axis='x', color='0.75')
        self.graphspan = 0
        if x < -200:
            self.graphspan_min = x -200
        else:
            self.graphspan_min = -200
        if self.boundary1 > self.height:
            self.graphspan = self.boundary1+200
        else:
            self.graphspan = self.height +200
        self.ax.axis('equal')
        self.ax.set_xlim(self.graphspan_min, self.graphspan+x)
        self.ax.set_ylim(-200, self.graphspan)
        y = 0.98
        # for entry in self.write_data:
        #    self.ax.text(0.65, y, entry,
        #                 horizontalalignment='left',
        #                 verticalalignment='center',
        #                 backgroundcolor='1.0',
        #                 size=14,
        #                 transform=self.ax.transAxes)
        #    y += -0.03
        plt.tight_layout()  # handy for fixing borders etc.
        plt.savefig(os.path.join('output',self.name+'_elevation'+'.png'), dpi=100)
        # PLAN
        self.pfig = plt.figure(figsize=(10, 10))
        plt.minorticks_on()
        self.pax = plt.subplot(111)
        self.rect = self.pfig.patch  # used to add a white background.Only for plt.show()
        self.rect.set_facecolor((1, 1, 1))
        #Walls
        self.pax.plot([-150, self.boundary3],[0, 0], linewidth=1.5, color='0')
        self.pax.plot([0, 0],[self.width, self.width+200], linewidth=1.5, color='0')
        self.pax.plot([self.boundary3, self.boundary3],
                      [0, self.boundary2], linewidth=1.5, color='0')
        self.pax.plot([self.boundary3, self.boundary3-self.boundary1],
                      [self.boundary2, self.boundary2], linewidth=1.5, color='0')
        self.pax.plot([0, 0], [0,self.width], linewidth=1.5, linestyle='--', color='0.0')
        #Top Flight
        self.pax.plot([self.overhang, self.overhang],
                     [0, self.width], linewidth=1.5, color='0.0')
        self.pax.plot([0, self.boundary3-self.width+40],[40, 40], linewidth=1.5, color='0.2')
        self.pax.plot([0, self.boundary3-self.width+40],
                     [self.width-40, self.width-40], linewidth=1.5, color='0.2')
        self.pax.plot([0, self.boundary3-self.width+40],
                     [self.width, self.width], linewidth=1.5, color='0.0')
        x = self.overhang+self.going
        for i in range(0, self.fl3_threads):
            self.pax.plot([x, x], [40, self.width-40], linewidth=1.5, color=(1, 0, 0))
            x += self.going
        self.pax.plot([self.boundary3+self.overlap2+40-self.width, self.boundary3-self.width+40],
                      [40, 40], linewidth=1.5, color=(1, 0, 0))
        self.pax.plot([self.boundary3+self.overlap2+40-self.width, self.boundary3-self.width+40],
                      [self.width-40, self.width-40], linewidth=1.5, color=(1, 0, 0))
        #Second Landing
        self.pax.plot([self.boundary3-self.width+40, self.boundary3-self.width+40],
                     [0, self.width+self.landing_protrusion], linewidth=1.5, linestyle='--', color=(1,0,0))
        self.pax.plot([self.boundary3-self.width+40, self.boundary3],
                     [self.width+self.landing_protrusion, self.width+self.landing_protrusion],
                      linewidth=1.5, color=(1,0,0))
        #Middle Flight
        self.pax.plot([self.boundary3-self.width+40, self.boundary3-self.width+40],
                     [self.width, self.boundary2-self.width+40], linewidth=1.5, color='0.2')
        self.pax.plot([self.boundary3-40, self.boundary3-40],
                     [self.width, self.boundary2 -self.width + 40], linewidth=1.5, color='0.2')
        self.pax.plot([self.boundary3-self.width, self.boundary3-self.width],
                     [self.width, self.boundary2-self.width+40], linewidth=1.5, color='0.0')
        y = self.width+self.going+self.landing_protrusion
        for i in range(0, self.fl2_threads):
            self.pax.plot([self.boundary3-self.width+40, self.boundary3-40],
                          [y, y], linewidth=1.5, color=(1, 0, 0))
            y += self.going
        self.pax.plot([self.boundary3-40, self.boundary3-40],
                      [self.boundary2+self.overlap+40-self.width, self.boundary2-self.width+40],
                      linewidth=1.5, color=(1, 0, 0))
        self.pax.plot([self.boundary3-self.width+40, self.boundary3-self.width+40],
                      [self.boundary2+self.overlap+40-self.width, self.boundary2-self.width+40],
                      linewidth=1.5, color=(1, 0, 0))
        #First Landing
        self.pax.plot([self.boundary3-self.width-self.landing_protrusion, self.boundary3],
                      [self.boundary2-self.width+40, self.boundary2-self.width+40],
                      linewidth=1.5, linestyle='--', color=(1,0,0))
        self.pax.plot([self.boundary3-self.width-self.landing_protrusion,
                       self.boundary3 -self.width-self.landing_protrusion],
                     [self.boundary2-self.width+40, self.boundary2],
                      linewidth=1.5, color=(1,0,0))
        #First Flight
        self.pax.plot([self.boundary3-self.width-self.landing_protrusion, self.boundary3-self.boundary1],
                      [self.boundary2-40, self.boundary2-40], linewidth=1.5, color='0.2')
        self.pax.plot([self.boundary3-self.width-self.landing_protrusion, self.boundary3-self.boundary1],
                      [self.boundary2-self.width+40, self.boundary2-self.width+40], linewidth=1.5, color='0.2')
        self.pax.plot([self.boundary3-self.width-self.landing_protrusion, self.boundary3-self.boundary1],
                      [self.boundary2-self.width, self.boundary2-self.width], linewidth=1.5, color='0.0')
        x = self.boundary3-self.width-self.landing_protrusion-self.going
        for i in range(0, self.fl1_threads):
            self.pax.plot([x, x], [self.boundary2-40, self.boundary2-self.width+40], linewidth=1.5, color=(1, 0, 0))
            x += -self.going

        self.pax.grid(True, 'major', linestyle="-", axis='y', color='0.65')
        self.pax.grid(True, 'major', linestyle="-", axis='x', color='0.65')
        self.pax.grid(True, 'minor', linestyle="--", axis='y', color='0.75')
        self.pax.grid(True, 'minor', linestyle="--", axis='x', color='0.75')
        self.graphspan = 0
        if x < -190:
            self.graphspan_min = x -200
        else:
            self.graphspan_min = -200
        if self.boundary1 > self.boundary2 or self.boundary3 > self.boundary2:
            self.graphspan = self.boundary1+200
            if self.boundary3 > self.boundary1:
                self.graphspan = self.boundary3+200
        else:
            self.graphspan = self.boundary2 +200
        self.pax.axis('equal')
        self.pax.set_xlim(self.graphspan_min, self.graphspan+x+200)
        self.pax.set_ylim(-200, self.graphspan)
        if self.turn == 'L':
            self.pax.set_ylim(self.graphspan, -200)
        plt.tight_layout()  # handy for fixing borders etc.
        plt.savefig(os.path.join('output',self.name+'_plan.png'), dpi=100)
        plt.show()
