#!/usr/bin/python
import math


cards = ['2','3','4','5','6','7','8','9','T','J','Q','K','A']
dir = ['S', 'W', 'N', 'E']
suits = ['S', 'H', 'D', 'C']
vul = {"o":"NONE", "e":"E-W", "n":"N-S", "b":"BOTH"}

class Link:
    def __init__(self, link):
        self.link = link
        self.player_list = self.get_player_list()
        self.dealer_id = self.get_dealer_id()
        self.dealer_dir = self.id_to_dir()
        self.hand_list = self.get_hand_list()
        self.hand_list = self.cal_east_hand()
        self.board_num = self.get_board_num()
        self.sv = self.get_sv()
        self.dealer = self.get_dealer()
        self.bidding_split = self.get_bidding_split()
        self.play_seq_split = self.get_play_seq_split()
    
    def id_to_dir(self):
        return dir[int(self.dealer_id)-1]

    def get_player_list(self):
        mystr = self.link
        player_start = mystr.find("pn|") + 3
        player_end = mystr.find("|st")
        player_list = mystr[player_start:player_end].split(",")
        return player_list

    def get_dealer_id(self):
        mystr = self.link
        hand_start = mystr.find("md|") + 4
        hand_end = mystr.find("|rh")
        dealer_id = mystr[hand_start-1:hand_start]
        return dealer_id

    def get_hand_list(self):
        mystr = self.link
        hand_start = mystr.find("md|") + 4
        hand_end = mystr.find("|rh")
        hand_list = mystr[hand_start:hand_end]
        hand_list = hand_list.split("%2C")
        return hand_list

    def cal_east_hand(self):
        hand_list = self.hand_list
        S = cards[:]
        H = cards[:]
        D = cards[:]
        C = cards[:]
        east_hand = ""
        for hand in hand_list:
            suit = ""
            for card in hand:
                if card=='S' or card=='H' or card=='D' or card=='C':
                    suit=card
                elif suit=='S':
                    S.remove(card)
                elif suit=='H':
                    H.remove(card)
                elif suit=='D':
                    D.remove(card)
                elif suit=='C':
                    C.remove(card)
        idx=0
        for hand in hand_list:
            east_hand = east_hand + suits[idx]
            if suits[idx]=='S':
                for card in S:
                    east_hand = east_hand + card
            elif suits[idx]=='H':
                for card in H:
                    east_hand = east_hand + card
            elif suits[idx]=='D':
                for card in D:
                    east_hand = east_hand + card
            elif suits[idx]=='C':
                for card in C:
                    east_hand = east_hand + card
            idx = idx + 1
    
        hand_list[3] = east_hand
        return hand_list

    def get_board_num(self):
        mystr = self.link
        return mystr[mystr.find("|ah|Board%20")+12:mystr.find("|sv|")]
    
    def get_sv(self):
        mystr = self.link
        return mystr[mystr.find("|sv|")+4:mystr.find("|sv|")+5]

    def get_dealer(self):
        return dir[(int(self.board_num) + 1)%4]

    def get_bidding_split(self):
        mystr = self.link
        deal_start = mystr[mystr.find("|sv|")+5:]
        bidding = deal_start[:deal_start.find("|pc|")]
        bidding = bidding.replace("|mb|", " ")
        bidding_split = bidding.split()
        return bidding_split

    def get_play_seq_split(self):
        mystr = self.link
        if mystr.find("|mc|") == -1:
            play_seq = mystr[mystr.find("|pc|")+4:len(mystr)-1]
        else:
            play_seq = mystr[mystr.find("|pc|")+4:mystr.find("|mc|")]
        play_seq_split = play_seq.split("|pc|")
        return play_seq_split

    


class Map:
    def __init__(self, board):
        self.map = []
        self.add_void_line()
        self.board = board
    
    def add_void_line(self):
        for i in range(0,21):
            void_line = ""
            self.map.append(void_line)

    def space_str(self, x):
        mystr=""
        for i in range(0, x):
            mystr=mystr+" "
        return mystr

    def print_list_to_map(self, st_line, l, sft):
        self.map
        sft_space = self.space_str(sft-len(self.map[st_line]))
        mystr = sft_space
        l.reverse()
        for c in l:
            mystr += c
        self.map[st_line] += mystr

    def analyze_hand(self, st_line, hand, sft):
        mystr = ""
        suit = ""
        S = []
        H = []
        D = []
        C = []
        sft_space = self.space_str(sft-len(self.map[st_line]))
        mystr += sft_space
        for card in hand:
            if card=='S' or card=='H' or card=='D' or card=='C':
                suit=card
            elif suit=='S':
                S.append(card)
            elif suit=='H':
                H.append(card)
            elif suit=='D':
                D.append(card)
            elif suit=='C':
                C.append(card)
        sft_space = self.space_str(sft-len(self.map[st_line]))
        self.map[st_line] += sft_space
        self.map[st_line] += "S "
        self.print_list_to_map(st_line, S, sft+2)
        sft_space = self.space_str(sft-len(self.map[st_line+1]))
        self.map[st_line+1] += sft_space
        self.map[st_line+1] += "H "
        self.print_list_to_map(st_line+1, H, sft+2)
        sft_space = self.space_str(sft-len(self.map[st_line+2]))
        self.map[st_line+2] += sft_space
        self.map[st_line+2] += "D "
        self.print_list_to_map(st_line+2, D, sft+2)
        sft_space = self.space_str(sft-len(self.map[st_line+3]))
        self.map[st_line+3] += sft_space
        self.map[st_line+3] += "C "
        self.print_list_to_map(st_line+3, C, sft+2)

    def print_North(self, st_line, player_id, hand):
        output_str = ""
        output_str = self.space_str(8)
        output_str += player_id
        self.map[st_line] += output_str
        st_line = st_line + 1
        self.analyze_hand(st_line, hand, 8)

    def print_West(self, st_line, player_id, hand):
        output_str = ""
        output_str += player_id
        self.map[st_line] += output_str
        st_line = st_line + 1
        self.analyze_hand(st_line, hand, 0)

    def print_East(self, st_line, player_id, hand):
        output_str = ""
        output_str = self.space_str(16-len(self.map[st_line]))
        output_str += player_id
        self.map[st_line] += output_str
        st_line = st_line + 1
        self.analyze_hand(st_line, hand, 16)

    def print_South(self, st_line, player_id, hand):
        output_str = ""
        output_str = self.space_str(8)
        output_str += player_id
        self.map[st_line] += output_str
        st_line = st_line + 1
        self.analyze_hand(st_line, hand, 8)

    def print_bidding(self, st_line, board_num, bidding_split):
        sft = 32 + ((int(board_num)+4)%4)*10
        self.map[st_line] += self.space_str(sft - len(self.map[st_line]))
        for bs in bidding_split:
            if bs == "d":
                self.map[st_line] += "X"
            elif bs == "r":
                self.map[st_line] += "XX"
            elif bs == "P":
                self.map[st_line] += "P"
            else:
                self.map[st_line] += bs
            self.map[st_line] += self.space_str(10-len(bs))
            if sft < 62:
                sft += 10
            else:
                sft = 32
                st_line += 1
                self.map[st_line] += self.space_str(sft - len(self.map[st_line]))

    def print_result(self, st_line):
        sft = 32
        self.map[st_line] += self.space_str(sft - len(self.map[st_line]))
        self.map[st_line] += "result"

    def print_play_seq(self, st_line):
        sft = 31
        output_str_title = ""
        
        output_str_title += self.space_str(sft - len(self.map[st_line]))
        round = int(math.ceil(len(self.board.play_seq_split)/4))
        output_str_title += self.space_str(2)
        for i in range(1, round+1):
            output_str_title += self.space_str(3-len(str(i)))
            output_str_title += str(i)
        self.map[st_line] += output_str_title
        output = {"W":"", "N":"", "E":"", "S":""}
        play_seqs = {"W":[], "N":[], "E":[], "S":[]}
        player_hands = []
        for hand in self.board.hand_list:
            hl = {"S":[], "H":[], "D":[], "C":[]}
            for card in hand:
                if card=='S' or card=='H' or card=='D' or card=='C':
                    suit=card
                else:
                     hl[suit].append(card)
            player_hands.append(hl)

        for idx, card in enumerate(self.board.play_seq_split):
            for idy, p in enumerate(player_hands):
                if card[1] in p[card[0]]:
                   if idx%4==0:
                       play_seqs[dir[idy]].append([card, 1])
                   else:
                       play_seqs[dir[idy]].append([card, 0])

        for d in dir:
            output[d] += d
            for c in play_seqs[d]:
                if c[1] == 1:
                    output[d] += "-"
                else:
                    output[d] += " "
                output[d] += c[0]

        for idx, d in enumerate(dir, start=1):
            self.map[st_line+idx] += self.space_str(sft - len(self.map[st_line+idx]) + 1)
            self.map[st_line+idx] += output[d]




    def print_map(self):
        print "============================================================================"
        self.map[0] = "Board " + self.board.board_num + ", dealer:" + self.board.dealer_dir + ", " + vul[self.board.sv]
        self.print_North(1, self.board.player_list[2], self.board.hand_list[2])
        self.print_West(6, self.board.player_list[1], self.board.hand_list[1])
        self.print_East(6, self.board.player_list[3], self.board.hand_list[3])
        self.print_South(11, self.board.player_list[0], self.board.hand_list[0])
        self.map[1] += self.space_str(32-len(self.map[1])) 
        self.map[1] += "W" + self.space_str(9) + "N" + self.space_str(9) + "E" + self.space_str(9) + "S"
        self.print_bidding(2, self.board.board_num, self.board.bidding_split)
        self.print_result(9)
        self.print_play_seq(11)
        
        for i in range(0, 21):
            print self.map[i]
        print "============================================================================"

def test(board):
    player_list = board.player_list
    print player_list

    dealer_id = board.dealer_id
    print dealer_id

    dealer_dir = board.dealer_dir
    print dealer_dir

    hand_list = board.hand_list
    print hand_list


    board_num = board.board_num
    print board_num

    sv = board.sv
    print vul[sv]

    dealer = board.dealer
    print dealer

    bidding_split = board.bidding_split
    print bidding_split

    play_seq_split = board.play_seq_split
    print play_seq_split



mystr = "http://www.bridgebase.com/tools/handviewer.html?bbo=y&lin=pn|pendala777,evileyes,jessica777,evileyes9|st||md|3S456QH579D8C2468J%2CS279KH8TJQAD46JCQ%2CSTAH46D2357QKAC9T%2C|rh||ah|Board%201|sv|o|mb|1D|mb|d|mb|1S|mb|3H|mb|d|mb|p|mb|3S|mb|d|mb|4D|mb|p|mb|p|mb|d|mb|p|mb|p|mb|p|pc|H2|pc|H5|pc|HA|pc|H4|pc|CQ|pc|C9|pc|C3|pc|C2|pc|HQ|pc|H6|pc|HK|pc|H7|pc|CK|pc|C4|pc|H8|pc|CT|pc|H3|pc|H9|pc|HT|pc|D2|pc|DA|pc|D9|pc|D8|pc|D4|pc|DK|pc|DT|pc|S4|pc|D6|pc|DQ|pc|C5|pc|C6|pc|DJ|pc|D7|pc|C7|pc|S5|pc|S2|pc|D5|pc|S3|pc|C8|pc|S7|pc|D3|pc|CA|pc|CJ|pc|HJ|pc|SA|pc|S8|pc|S6|pc|S9|pc|ST|pc|SJ|pc|SQ|pc|SK|"

mystr1 = "http://www.bridgebase.com/tools/handviewer.html?bbo=y&lin=pn|pendala777,evileyes,jessica777,evileyes9|st||md|1S69H4TJD27QKC39JQ%2CS3H269KAD458JC678%2CS57QKAH57D39C25KA%2C|rh||ah|Board%203|sv|e|mb|p|mb|p|mb|1S|mb|p|mb|1N|mb|p|mb|2C|mb|p|mb|2S|mb|p|mb|2N|mb|p|mb|3N|mb|p|mb|p|mb|p|pc|H6|pc|H5|pc|HQ|pc|H4|pc|H8|pc|HT|pc|HK|pc|H7|pc|HA|pc|D3|pc|H3|pc|HJ|pc|H9|pc|C2|pc|C4|pc|D2|pc|H2|pc|D9|pc|CT|pc|D7|pc|C6|pc|CA|pc|D6|pc|C3|pc|SA|pc|S2|pc|S6|pc|S3|pc|SK|pc|S4|pc|S9|pc|D4|pc|SQ|mc|7|"

mystr = raw_input(">>> Link: ")


board = Link(mystr)
#test(board)

map = Map(board)
map.print_map()


