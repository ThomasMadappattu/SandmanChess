import Tkinter
import Tkinter as Tk
from Tkinter import *
import chess
import chess.uci
import chess.pgn
import os
import random
import telnetlib
import tkFileDialog
import tkMessageBox
import functools
from StringIO import StringIO
import fileinput
import time

class UIConstants:
        def __init__(self):
                self.PlayerMode = 0
                self.AnalysisMode = 1
                self.NetworkMode = 2
                self.PgnMode  = 3
                self.TutorMode = 4
                self.ServerTypeFICS = 5
                self.ServerTypeICC = 6
                self.FICSServerHost = "freechess.org"
                self.FICSPort = 5000
                


class ChessEnginePlayer:
        def set_board(self,brd):
                self.chessBoard = brd
                self.engineDepth = 1
                self.timemS = 1000
        def start_new_game(self):
                self.engine.ucinewgame()
        def set_engine_path(self, path):
                self.engine = chess.uci.popen_engine(path)
                self.engine.uci()
                self.start_new_game()
        def set_engine_depth(self, depth):
                self.engineDepth = depth
        def set_time_millisecond( self, time):
                self.timemS = time
        def set_time_seconds(self, seconds):
                self.set_time_millisecond(seconds* 1000)
        def get_move(self):
                self.engine.position(self.chessBoard)
                self.bestMove, self.ponderMove = self.engine.go( depth=self.engineDepth)
                return self.bestMove
                

class NetworkPlayer:
        def __init__(self):
                self.Constants = UIConstants()
                self.current_line =' '  
        def login_fics(self,username,password):
                self.telnetHandle = telnetlib.Telnet(self.Constants.FICSServerHost)
                self.telnetHandle.read_until("login:")
                self.telnetHandle.write(username+"\r\n")
                self.telnetHandle.read_until("password:")
                self.telnetHandle.write(password+"\r\n")
                #self.telnetHandle.write("set style 12 \r\n")
        def parse_style_12(self,style12_str):
                pass
        def read_line(self):
                self.current_line = self.telnetHandle.read_until("\n",timeout=2)
                print(self.current_line) 
                return self.current_line
        def send_command(self,command):
                self.telnetHandle.write(command+"\r\n")

        def set_board(self,brd):
                self.chessBoard = brd
        def set_type ( self, serverType):
                self.netType = serverType
        def set_username( self, username):
                self.username = username
        def set_password( self, pwd):
                self.password = pwd
        def login():
                pass
        def get_move(self):
                pass

class  WoodPusherAI:
        def set_board(self,brd):
                self.chessBoard = brd
        def start_new_game(self):
                pass
        def get_move(self):
                moves = self.chessBoard.legal_moves
                movesLen = len( self.chessBoard.legal_moves)
                self.move = None
                count  = 0 
                if ( movesLen  > 0 ):
                        index = random.randint(0,len( self.chessBoard.legal_moves)-1)
                        for mv in self.chessBoard.legal_moves:
                           if( count == index ):
                                   self.move = mv
                           count = count + 1
                        return self.move
                return None


class Player:
         
        def __init__(self,board):
                self.chessBoard = Board()
        def set_personality(self,PType):
                self.personalityType = PType
        def get_move(self):
                return self.personalitytype.get_move()

class TrainingPuzzle:
        def __init__(self):
                self.sovled = False
                self.visited = False

class LucasFnsParser:
    def __init__(self):
        self.FenIndex = 0
        self.DescriptionIndex = 1
        self.MovesIndex = 2
        self.currentItem=[]
        self.fnsLines = list()
    
    def GetFnsLines(self,filename):
        for item in fileinput.input(filename):
            self.fnsLines.append(item)
    def ParseFnsItem(self,item,fnsLine):
        self.currentItem = str(fnsLine).split('|')
    def GetcurrentFen(self):
        return self.currentItem[self.FenIndex]
    def GetCurrentDescription(self):
        if ( len(self.currentItem) > 1 ):
            return self.currentItem[self.DescriptionIndex]
        return None
    def GetCurrentMoves(self):
        if ( len(self.currentItem> 2)):
            return self.currentItem[self.MovesIndex]
        return None
    def setCurrentItem(self,index):
        if ( index< len(self.fnsLines)-1):
            self.currentItem = self.fnsLines[index]
    def GetPgn(self):
            pgnString='[Event "?"]\r\n[Site "?"]\r\n[Date "????.??.??"]\r\n[Round "?"]\r\n[White "?"][Black "?"]\r\n[Result "*"][Fen="%s"]\r\n%s'%(self.GetcurrentFen(),self.GetCurrentMoves())
            print(pgnString)
            return pgnString


class PgnItem:
        def __init__(self,header,offset):
                self.header = header
                self.offset = offset



class LoginDialog:
    def __init__(self,parent,parentUI):
        self.LoginFrame = Toplevel(parent)
        self.parent = parent
        self.parentUI = parentUI
        self.UserNameLabel = Label(self.LoginFrame,text="Username:").grid(row=0)
        self.PasswordLabel = Label(self.LoginFrame,text="Password:").grid(row=1)
        self.UserNameTextBox = Entry(self.LoginFrame,width=25)
        self.UserNameTextBox.grid(row=0,column=1)
        self.PasswordTextBox = Entry(self.LoginFrame,show="*",width=25)
        self.PasswordTextBox.grid(row=1,column=1)
        self.LoginButton     = Button(self.LoginFrame,text="Login",command=self.login_pressed).grid(row=2,column=0)
        self.CancelButton    = Button(self.LoginFrame,text="Cancel",command=self.cancel_pressed).grid(row=2,column=1)
    def cancel_pressed(self):
        self.LoginFrame.destroy()
    def login_pressed(self):
        self.parentUI.network_player = NetworkPlayer()
        self.parentUI.network_player.login_fics(self.UserNameTextBox.get(),self.PasswordTextBox.get())
        self.LoginFrame.destroy()
         

class NetworkInterfaceDialog:
    def __init__(self,parent,network_player):
        self.network_player= network_player
        self.NetworkFrame = Toplevel(parent)
        self.TelenetMessages = Text(self.NetworkFrame,width=90,height=40)
        self.TelenetMessages.pack()
        self.CommandEntry = Entry(self.NetworkFrame,width=30)
        self.CommandEntry.pack()
        self.SendButton = Button(self.NetworkFrame,text="Send",command=self.send_button_pressed)
        self.SendButton.pack(side=LEFT) 
        self.NetworkFrame.after(500,self.update_messages)
        self.line_count = 0 
    def send_button_pressed(self):
        self.network_player.send_command(self.CommandEntry.get())
    def update_messages(self):
        currentLine = self.network_player.read_line()
        self.TelenetMessages.insert(END,currentLine.strip()+"\n")
        self.TelenetMessages.see(END)
        self.line_count = self.line_count + 1 
        if ( self.line_count > 5000 ):
            self.TelenetMessages.delete(1.0,END)
            self.line_count = 0
        self.NetworkFrame.after(500,self.update_messages)



class PromotionDialog:
        def __init__(self,parentUI,color):
                self.promotionFrame = Toplevel()
                self.parentUI = parentUI 
                if ( color == chess.BLACK ):
                        self.QueenButton = Button (self.promotionFrame,width=parentUI.squareLen,height=parentUI.squareLen, image=parentUI.theme.BlackQueen, command =  lambda:self.handlePButtonClick('q'))
                        self.QueenButton.pack()
                        self.RookButton = Button (self.promotionFrame,width=parentUI.squareLen,height=parentUI.squareLen, image=parentUI.theme.BlackRook, command =  lambda:self.handlePButtonClick('r'))
                        self.RookButton.pack()
                        self.BishopButton = Button (self.promotionFrame,width=parentUI.squareLen,height=parentUI.squareLen, image=parentUI.theme.BlackBishop, command =  lambda:self.handlePButtonClick('b'))
                        self.BishopButton.pack()
                        self.KnightButton = Button (self.promotionFrame,width=parentUI.squareLen,height=parentUI.squareLen, image=parentUI.theme.BlackKnight, command =  lambda:self.handlePButtonClick('n'))
                        self.KnightButton.pack()
                elif ( color == chess.WHITE):
                        self.QueenButton = Button (self.promotionFrame,width=parentUI.squareLen,height=parentUI.squareLen, image=parentUI.theme.WhiteQueen, command =  lambda:self.handlePButtonClick('Q'))
                        self.QueenButton.pack()
                        self.RookButton = Button (self.promotionFrame,width=parentUI.squareLen,height=parentUI.squareLen, image=parentUI.theme.WhiteRook, command =  lambda:self.handlePButtonClick('R'))
                        self.RookButton.pack()
                        self.BishopButton = Button (self.promotionFrame,width=parentUI.squareLen,height=parentUI.squareLen, image=parentUI.theme.WhiteBishop, command =  lambda:self.handlePButtonClick('B'))
                        self.BishopButton.pack()
                        self.KnightButton = Button (self.promotionFrame,width=parentUI.squareLen,height=parentUI.squareLen, image=parentUI.theme.WhiteKnight, command =  lambda:self.handlePButtonClick('N'))
                        self.KnightButton.pack()
                self.promotionFrame.resizable(0,0)
                self.promotionFrame.wait_window()

        def handlePButtonClick(self,pieceSymbol):
                self.parentUI.promotionPiece = chess.Piece.from_symbol(pieceSymbol)
                self.promotionFrame.destroy()

class PgnDialog:
        def __init__(self,parentUI,pgn_list):
                self.pgnFrame = Toplevel(width=50)
                self.parentUI = parentUI
                self.pgn_item_list = pgn_list
                self.FilterFrame = Frame(self.pgnFrame) 
                self.FilterLabel = Label(self.FilterFrame,text="Filter:")
                self.FilterLabel.pack(side=LEFT)
                self.FilterEntry = Entry (self.FilterFrame,width=60)
                self.FilterEntry.pack(side=LEFT)
                self.FilterEntry.bind('<Return>',lambda(event):self.filter_pressed())
                self.FilterButton = Button(self.FilterFrame,text="Filter",anchor='w',command=self.filter_pressed)
                self.FilterButton.pack(anchor='w',side=LEFT)
                self.FilterFrame.pack()
                self.GameListFrame = Frame(self.pgnFrame)
                self.ListScrollBar = Scrollbar(self.GameListFrame)
                self.ListScrollBar.pack(side=RIGHT)
                self.GameListBox = Listbox(self.GameListFrame,width=100,yscrollcommand=self.ListScrollBar.set)
                self.GameListBox.bind('<Return>',lambda(event):self.ok_pressed())
                self.ListScrollBar.config(command=self.GameListBox.yview)
                for item in self.pgn_item_list:
                        self.GameListBox.insert(END,item.header)
                self.GameListBox.pack()
                self.GameListFrame.pack()
                self.OkButton = Button(self.pgnFrame,text="OK",command=self.ok_pressed)
                self.OkButton.pack()
                self.filtered_list  = list()
                self.pgnFrame.resizable(0,0)
        def ok_pressed(self):
                self.currentSelection  = self.GameListBox.curselection()
                if ( len(self.filtered_list) <= 0 ):
                    self.filtered_list = self.pgn_item_list
                    if ( len(self.filtered_list) <= 0):
                        return
                print(self.currentSelection)
                if ( len(self.currentSelection) <= 0 ):
                        tkMessageBox.showinfo(" Please","select a game ")
                        return
                else:
                        self.currentSelection = self.currentSelection[0]
                self.parentUI.pgn_file.seek(self.filtered_list[self.currentSelection].offset)
                self.parentUI.pgnGame = chess.pgn.read_game(self.parentUI.pgn_file)
                self.parentUI.currentGameNode = self.parentUI.pgnGame
                self.parentUI.chessBoard = self.parentUI.pgnGame.board()
                self.current_pgn_index = 0 
                self.parentUI.draw_main_board()
                self.parentUI.txtPgn.config(state=NORMAL)
                self.parentUI.txtPgn.delete(1.0,END)
                self.parentUI.txtPgn.insert(END,str(self.parentUI.pgnGame))
                self.parentUI.txtPgn.config(state=DISABLED)
                self.pgnFrame.destroy()

                
        def filter_pressed(self):
                self.filtered_list = list()
                filter_text = self.FilterEntry.get()
                self.GameListBox.delete(0,END)

                for item in self.pgn_item_list:
                    if ( re.search(filter_text,item.header) != None):
                        self.filtered_list.append(PgnItem(item.header,item.offset))
                for item in self.filtered_list:
                    self.GameListBox.insert(END,item.header)
                
            

                
                
                
class BoardColor:
    def __init__(self,colorWhite,colorBlack):
        self.colorWhite = colorWhite
        self.colorBlack = colorBlack
    def SetColorGreen(self):
        self.colorBlack = "#769656"
        self.colorWhite = "#eeeed2"
    def SetColorBrown(self):
        self.colorBlack = "#A66D4F"
        self.colorWhite = "#DDB88C"
    def SetColorPurple(self):
        self.colorBlack = "#660099"
        self.colorWhite = "#eeeed2"
    

class GuiTheme:
        def get_themes(self,themeDir):
                theme_list = list()
                for item in os.listdir(themeDir):
                        if ( len (item) > 2 ):
                                theme_list.append(item)
                return theme_list
        def __init__(self,themeDir):
                self.WhitePawn = PhotoImage(file=os.path.join(str(themeDir),"wp.gif"))
                self.BlackPawn = PhotoImage(file=os.path.join(str(themeDir),"bp.gif"))
                self.WhiteBishop = PhotoImage(file=os.path.join(str(themeDir),"wB.gif"))
                self.BlackBishop = PhotoImage(file=os.path.join(str(themeDir),"bB.gif"))
                self.WhiteRook   = PhotoImage( file =os.path.join(str(themeDir),"wR.gif"))
                self.BlackRook   = PhotoImage( file = os.path.join (str(themeDir), "bR.gif"))
                self.WhiteKnight = PhotoImage (file = os.path.join (str(themeDir),"wN.gif" ))
                self.BlackKnight = PhotoImage ( file = os.path.join (str(themeDir), "bN.gif"))
                self.BlackQueen =  PhotoImage ( file = os.path.join (str(themeDir), "bQ.gif"))
                self.WhiteQueen =  PhotoImage ( file = os.path.join (str(themeDir), "wQ.gif"))
                self.BlackKing =  PhotoImage ( file = os.path.join (str(themeDir), "bK.gif"))
                self.WhiteKing =  PhotoImage ( file = os.path.join (str(themeDir), "wK.gif"))
                
                

class SandmanGui:
        def __init__(self,parent):
                self.rows = 8 
                self.columns = 8 
                self.colorWhite = "#DDB88C"
                self.colorBlack = "#A66D4F"
                self.totalSquares = 64
                self.squareLen = 70
                self.clickedBoard = 0
                self.chessBoard = chess.Board()
                self.adjust =  self.squareLen/2
                self.startRow = 0
                self.endRow = 0
                self.startCol = 0
                self.endCol = 0
                self.player = None
                self.mode  = 0
                self.promotionPiece = None
                self.flip = False 
                self.playerMovesFirst = False
                self.enginePath = None
                self.themeDir="./themes"
                self.theme = None
                self.themeList = list()
                self.boardColors = BoardColor(self.colorWhite,self.colorBlack)
                self.pgnGame  = None
                self.pgn_file = None
                self.currentGameNode = None
                self.parent = parent
                self.pgn_item_list = None
                self.current_pgn_index = 0
                self.pgn_stop = False
                self.network_player = None 
        def init_board(self ,parentGui):
                self.parent = parentGui
                self.theme  = GuiTheme(os.path.join(self.themeDir,'boring'))
                self.menubar = Menu(self.parent)
                self.filemenu = Menu(self.menubar,tearoff=0)
                self.filemenu.add_command(label="Flip Board",command = self.menu_flip_board)
                self.filemenu.add_command(label="Reset Board", command = self.reset_board)
                self.filemenu.add_command(label="Exit", command=self.exit_chess)
                self.menubar.add_cascade(label="File", menu = self.filemenu)
                self.playerMenu = Menu (self.parent)
                self.playerMenu.add_command(label="Woodpusher", command = self.set_woodpusher)
                self.playerMenu.add_command(label="Choose Engine", command = self.set_external_engine)
                self.menubar.add_cascade(label="Players", menu=self.playerMenu)
                self.themeMenu = Menu ( self.parent)
                self.menubar.add_cascade ( label = "Themes", menu = self.themeMenu)
                for item in self.theme.get_themes( self.themeDir):
                    self.themeMenu.add_command ( label = item, command = functools.partial(self.set_theme,item,True))
                self.themeMenu.add_command( label = "Brown Board", command = lambda: self.set_board_color("brown"))
                self.themeMenu.add_command(label = "Green Board" ,command = lambda: self.set_board_color("green"))
                self.themeMenu.add_command(label = "Purple Board", command = lambda: self.set_board_color("purple"))

                self.networkMenu  =  Menu ( self.parent )
                self.menubar.add_cascade ( label = "Network", menu = self.networkMenu)
                self.networkMenu.add_command(label = "FICS",command=self.fics_pressed)
                self.networkMenu.add_command(label = "ICC")
                self.trainingMenu  =  Menu (self.parent)
                self.menubar.add_cascade ( label = "Training", menu = self.trainingMenu)
                self.pgnMenu  =  Menu ( self.parent)
                self.pgnMenu.add_command(label="Open PGN", command=self.handle_open_pgn)
                self.pgnMenu.add_command(label="List PGN Games", command = self.list_pgn_games)
                self.menubar.add_cascade ( label = "PGN", menu = self.pgnMenu )
                
                self.canvas = Canvas ( self.parent, width = self.rows * self.squareLen, height = self.columns * self.squareLen, background = "grey")
                self.canvas.pack(padx = 8,pady= 8)
                self.buttonPanel =  Frame(self.parent)
                self.PgnStartButton =  Button(self.buttonPanel,text="<<",width=2,command=self.start_button_pressed)
                self.PgnStartButton.pack(side = LEFT)
                self.PgnPrevButton = Button(self.buttonPanel,text ="<",width=2,command=self.prev_button_pressed)
                self.PgnPrevButton.pack(padx=3,side= LEFT)
                self.PgnNextButton = Button (self.buttonPanel, text =">",width=2,command=self.next_button_pressed)
                self.PgnNextButton.pack(padx=3,side=LEFT)
                self.PgnEndButton= Button (self.buttonPanel,text =">>",width=3,command=self.end_button_pressed)
                self.PgnEndButton.pack(padx=3,side=LEFT)
                self.SolveButton =Button(self.buttonPanel,text="Solve",width=4)
                self.SolveButton.pack(padx=3,side=LEFT)
                self.NextGameButton = Button (self.buttonPanel,text=">>Game",width=4,command=self.next_game_pressed)
                self.NextGameButton.pack(padx=3,side=LEFT)
                self.PrevGameButton = Button(self.buttonPanel,text="<<Game",width=4,command=self.prev_game_pressed)
                self.PrevGameButton.pack(padx=3,side=LEFT)
                self.PlayButton = Button(self.buttonPanel,text="[>]",width=2,command=self.pgn_play_pressed)
                self.PlayButton.pack(padx=3,side=LEFT)
                self.StopButton = Button( self.buttonPanel,text="[]",width=2,command=self.stop_button_pressed)
                self.StopButton.pack(padx=3,side=LEFT)
                self.buttonPanel.pack()
                self.infoFrame = Frame(self.parent)
                self.txtPgn     = Text(self.infoFrame,height=10)
                #self.infoLabel =  Label(self.infoFrame,width=100)
                #self.infoLabel.pack(side=BOTTOM)
                self.draw_main_board()
                self.parent.config( menu = self.menubar)
                self.txtPgn.pack(side=TOP)
                self.infoFrame.pack(side=TOP)
                self.canvas.bind("<Button-1>", self.board_clicked)
                
        def menu_flip_board(self):
                self.flip_board()
                self.draw_main_board()
                
        def canvas_click_toggle(self):
                if ( self.clickedBoard == 0 ):
                        self.clickedBoard = 1
                else:
                        self.clickedBoard = 0

        def set_board_color(self,colorScheme):
            if ( colorScheme == "brown"):
                self.boardColors.SetColorBrown()
            elif ( colorScheme == "green"):
                self.boardColors.SetColorGreen()
            else:
                self.boardColors.SetColorPurple()
            self.colorWhite = self.boardColors.colorWhite
            self.colorBlack = self.boardColors.colorBlack
            self.draw_main_board()

        def board_clicked( self,event):
                posx = event.x
                posy = event.y
                row = posx / self.squareLen
                col = posy /self.squareLen
                startx = row * self.squareLen
                starty = col * self.squareLen
                endx = startx + self.squareLen
                endy = starty + self.squareLen
                self.draw_main_board()
                if ( self.clickedBoard == 0 ):
                        self.startRow = row
                        self.startCol = col
                        self.canvas.create_rectangle(startx, starty, endx, endy,width=5.0)
                else:
                        self.endRow = row
                        self.endCol = col
                        currentMove = chess.Move.from_uci(self.get_move_uci())
                        print(currentMove)
                        moveLegal = currentMove in self.chessBoard.legal_moves
                        if ( moveLegal ):
                                self.chessBoard.push(currentMove)
                                print(self.chessBoard)
                                print(self.chessBoard.fen()) 
                                self.draw_main_board()
                                Tk.update(self.parent)
                        self.draw_main_board()
                        
                        
                        if ( self.chessBoard.is_checkmate()):
                                self.display_victory_message()
                        if ( self.player is not None and (moveLegal) ):
                                playerMove= self.player.get_move()
                               
                                if ( playerMove is not None ):
                                        self.chessBoard.push(playerMove)
                                        self.draw_main_board()
                                        if( self.chessBoard.is_checkmate()):
                                                self.display_victory_message()
                self.canvas_click_toggle()
                self.promotionPiece = None

        def reset_board(self):
                self.chessBoard = chess.Board()
                self.draw_main_board()
                if self.player is not None:
                        self.player.set_board(self.chessBoard)
                        self.player.start_new_game()
        def display_victory_message(self):
                if ( self.chessBoard.turn == chess.WHITE):
                        tkMessageBox.showinfo("Result!", "Black Wins")
                else:
                        tkMessageBox.showinfo("Result!","White Wins")

        def get_square_from_row_col( self, row, col ):
                if ( self.flip):
                        return chr ( ord('h') -row ) + chr ( ord('1') + (col ) ) 
                return chr ( ord('a')+ row  ) + chr ( ord('1') + (7 - col ) )
        def get_chess_py_sq_from_row_col( self, row,col):
                if ( self.flip):
                        return ( col * 8 + (7 -row) )
                return  ( (7-col) * 8 + row )
        def is_pawn_promotion( self, turn, fromPiece, endCol):
                if ( self.flip):
                        if ( self.chessBoard.turn == chess.BLACK and fromPiece == chess.PAWN and self.endCol == 0 ):
                                return True
                        elif ( self.chessBoard.turn ==  chess.WHITE and fromPiece == chess.PAWN and self.endCol == 7):
                                return True
                        return False
                else:
                        if ( self.chessBoard.turn == chess.BLACK and fromPiece == chess.PAWN and self.endCol == 7 ):
                                return True
                        elif ( self.chessBoard.turn == chess.WHITE and fromPiece == chess.PAWN and self.endCol == 0 ):
                                return True
                        return False
                        
                        
                        
        
        def get_move_uci(self):
                fromSquare = self.get_square_from_row_col(self.startRow,self.startCol)
                toSquare   = self.get_square_from_row_col(self.endRow,self.endCol)
                fromPiece  = self.chessBoard.piece_type_at(self.get_chess_py_sq_from_row_col(self.startRow,self.startCol))
                if ( self.chessBoard.turn == chess.BLACK and self.is_pawn_promotion(self.chessBoard.turn,fromPiece,self.endCol)):
                        self.handle_promotion(chess.BLACK)
                elif ( self.chessBoard.turn == chess.WHITE and self.is_pawn_promotion(self.chessBoard.turn,fromPiece,self.endCol)):
                        self.handle_promotion(chess.WHITE)
                if ( self.promotionPiece is not None):
                    return fromSquare + toSquare + self.promotionPiece.symbol().lower()
                return fromSquare + toSquare
                 
                
                
        def draw_player_move_first(self):
                if ( self.playerMovesFirst):
                        currentMove = self.player.get_move()
                        self.chessBoard.push(currentMove)
                        self.draw_main_board()
                
        
        def draw_main_board(self):
                sq_color = 0
                for r in range (self.rows):
                        for c in range(self.columns):
                                xpos = c * self.squareLen
                                ypos = r * self.squareLen
                                xend = xpos + self.squareLen
                                yend= ypos + self.squareLen
                                if ( ( c + r) % 2 == 0 ):
                                        sq_color = self.colorWhite
                                else:
                                        sq_color = self.colorBlack
                                self.canvas.create_rectangle(xpos,ypos,xend, yend, fill = sq_color, tags ="area" )
                                piece = self.chessBoard.piece_at( self.pos_to_brd_square(xpos,ypos) )
                                if ( piece != None):
                                        self.draw_piece( xpos+ self.adjust, ypos + self.adjust,piece )
                                        
        def pos_to_brd_square(self, xpos, ypos):
                if ( self.flip ):
                        row = 7 - xpos/self.squareLen
                        col = ypos/self.squareLen
                else:
                        row = xpos/ self.squareLen
                        col = 7 - ypos/ self.squareLen
                return ( col * 8 + row )
                                
        def draw_piece(self,x_pos, y_pos, piece):
                if ( piece.symbol() == 'p'):
                        self.canvas.create_image( x_pos,y_pos, image = self.theme.BlackPawn, state = Tkinter.NORMAL)
                elif ( piece.symbol() == 'k'):
                        self.canvas.create_image( x_pos,y_pos, image = self.theme.BlackKing, state = Tkinter.NORMAL)
                elif ( piece.symbol() == 'q'):
                        self.canvas.create_image( x_pos,y_pos, image = self.theme.BlackQueen, state = Tkinter.NORMAL)
                elif ( piece.symbol() == 'n' ):
                        self.canvas.create_image ( x_pos, y_pos, image = self.theme.BlackKnight, state = Tkinter.NORMAL)
                elif ( piece.symbol() == 'r'):
                        self.canvas.create_image( x_pos, y_pos, image = self.theme.BlackRook, state = Tkinter.NORMAL)
                elif ( piece.symbol() == 'b'):
                        self.canvas.create_image( x_pos, y_pos, image = self.theme.BlackBishop, state = Tkinter.NORMAL)
                elif ( piece.symbol() == 'P'):
                        self.canvas.create_image( x_pos,y_pos, image = self.theme.WhitePawn, state = Tkinter.NORMAL)
                elif ( piece.symbol() == 'K'):
                        self.canvas.create_image( x_pos,y_pos, image = self.theme.WhiteKing, state = Tkinter.NORMAL) 
                elif ( piece.symbol() == 'R'):
                        self.canvas.create_image( x_pos,y_pos, image = self.theme.WhiteRook, state = Tkinter.NORMAL)
                elif ( piece.symbol() == 'B'):
                        self.canvas.create_image( x_pos,y_pos, image = self.theme.WhiteBishop, state = Tkinter.NORMAL)
                elif ( piece.symbol() == 'N'):
                        self.canvas.create_image( x_pos,y_pos, image = self.theme.WhiteKnight, state = Tkinter.NORMAL)
                elif ( piece.symbol() == 'Q'):
                       self.canvas.create_image( x_pos,y_pos, image = self.theme.WhiteQueen, state = Tkinter.NORMAL)
                        
                        
        def set_player(self, player):
                self.player = player

        def set_woodpusher_player(self):
                ai = WoodPusherAI()
                ai.set_board(self.chessBoard)
                self.set_player(ai)
        def set_woodpusher(self):
                self.set_woodpusher_player()
                self.decide_who_plays()
                
        def set_engine_player(self):
                ai = ChessEnginePlayer()
                ai.set_engine_path(self.enginePath)
                ai.set_board(self.chessBoard)
                self.set_player(ai)
                

        def handle_promotion(self,turn):
            PromotionDialog(self,turn)
            
        def set_external_engine(self):
            self.enginePath=tkFileDialog.askopenfile(mode='r').name
            try:
                    self.set_engine_player()
            except:
                    tkMessageBox.showerror("Error", "Could not intialize!")
            self.decide_who_plays() 
           
            
        def decide_who_plays(self):
            if tkMessageBox.askyesno(" White ?", "Engine plays White  ?"):
                    self.playerMovesFirst = True
                    self.draw_player_move_first()
                        
        def exit_chess(self):
                self.parent.destroy()
                
        def set_theme(self,themename,redraw):
                self.theme = GuiTheme(os.path.join(self.themeDir, themename))
                if ( redraw):
                    self.draw_main_board()
                
        def set_player(self, playerType):
                self.player = playerType

        def flip_board(self):
                if (self.flip):
                        self.flip = False
                else:
                        self.flip = True

        def handle_open_pgn(self):
                self.pgn_file = tkFileDialog.askopenfile(mode='r')
                self.header_list = list()
                self.offset_list = list()
                self.pgn_item_list = list()
                print(self.pgn_file)
                for offset,headers in chess.pgn.scan_headers(self.pgn_file):
                        header_string = ""
                        for key in headers.keys():
                            header_string +=str(headers[key]) + "  "
                        header_string +="\n"
                        self.header_list.append(header_string)
                        print(headers.keys)
                        self.offset_list.append(offset)
                        self.pgn_item_list.append(PgnItem(header_string,offset))
                self.pgnDialog = PgnDialog(self,self.pgn_item_list)
                
        def list_pgn_games(self):
                if ( self.pgn_item_list is not None):
                        self.pgnDialog = PgnDialog(self,self.pgn_item_list)
                else:
                        tkMessageBox.showinfo("Sandmanchess","PGN not loaded")
        def prev_button_pressed(self):
                if self.pgnGame is not None:
                        if ( self.currentGameNode.parent is not None):
                                self.currentGameNode = self.currentGameNode.parent
                                self.chessBoard = self.currentGameNode.board()
                                self.draw_main_board()
                        
                pass
        def next_button_pressed(self):
                if self.pgnGame is not None:
                        if (self.currentGameNode is not None ):
                                if( len(self.currentGameNode.variations) > 0 ):
                                    for variation in self.currentGameNode.variations:
                                            if variation.is_main_line():
                                                    self.currentGameNode = variation
                                                    if ( variation.move is not None):
                                                            self.draw_move_arrow(variation.move)
                                                            Tk.update(self.parent)
                                                            time.sleep(0.25)
                                                    self.chessBoard=self.currentGameNode.board()
                                                    self.draw_main_board()
        def start_button_pressed(self):
                if self.pgnGame is not None:
                        self.currentGameNode = self.pgnGame
                        self.chessBoard  = self.currentGameNode.board()
                        self.draw_main_board()
        def end_button_pressed(self):
                if  self.pgnGame is not None:
                        self.currentGameNode = self.currentGameNode.end()
                        self.chessBoard = self.currentGameNode.board()
                        self.draw_main_board()

        def draw_move_arrow(self,move):
                move_str = str(move)
                start_sq = move_str[0:2]
                end_sq = move_str[2:4]
                if ( self.flip):
                        start_x = (7 - (ord(start_sq[0]) - ord('a'))) * self.squareLen + self.squareLen/2
                        end_x  =  (7 - ( ord(end_sq[0]) - ord('a'))) * self.squareLen + self.squareLen/2 
                        start_y =  (( ord(start_sq[1]) - ord('1') )) * self.squareLen + self.squareLen/2
                        end_y =   ((ord(end_sq[1]) - ord('1'))) * self.squareLen + self.squareLen/2
                else:
                        start_x = (ord(start_sq[0]) - ord('a')) * self.squareLen + self.squareLen/2
                        end_x  =  (ord(end_sq[0]) - ord('a')) * self.squareLen + self.squareLen/2
                        start_y =  (7-( ord(start_sq[1]) - ord('1') )) * self.squareLen + self.squareLen/2
                        end_y =   (7-(ord(end_sq[1]) - ord('1'))) * self.squareLen + self.squareLen/2        
                
              
                self.canvas.create_line(start_x,start_y,end_x,end_y,arrow=LAST,arrowshape=(15,15,15),fill='blue',width=10.0)
        def next_game_pressed(self):
                if ( self.pgn_item_list is not None):
                        pgn_item_max_index = len(self.pgn_item_list) - 1
                        self.current_pgn_index = min( (self.current_pgn_index+1),pgn_item_max_index )
                        self.pgn_file.seek(self.pgn_item_list[self.current_pgn_index].offset)
                        self.pgnGame = chess.pgn.read_game(self.pgn_file)
                        self.chessBoard = self.pgnGame.board()
                        self.currentGameNode = self.pgnGame
                        self.txtPgn.config(state=NORMAL)
                        self.txtPgn.delete(1.0,END)
                        self.txtPgn.insert(END,str(self.pgnGame))
                        self.txtPgn.config(state=DISABLED)
                        self.draw_main_board()
        def prev_game_pressed(self):
                if ( self.pgn_item_list is not None):
                        self.current_pgn_index = max( (self.current_pgn_index-1),0 )
                        self.pgn_file.seek(self.pgn_item_list[self.current_pgn_index].offset)
                        self.pgnGame = chess.pgn.read_game(self.pgn_file)
                        self.chessBoard = self.pgnGame.board()
                        self.currentGameNode = self.pgnGame
                        self.txtPgn.config(state=NORMAL)
                        self.txtPgn.delete(1.0,END)
                        self.txtPgn.insert(END,str(self.pgnGame))
                        self.txtPgn.config(state=DISABLED)
                        self.draw_main_board()
        def pgn_play_pressed(self, nextTime=False):
                if ( self.currentGameNode is not None):
                        if ( self.pgn_stop ):
                                self.pgn_stop = False
                                if(nextTime):
                                        return 
                        if ( len( self.currentGameNode.variations)> 0):
                                self.next_button_pressed()
                                self.parent.after(2000,lambda:self.pgn_play_pressed(True))
        def stop_button_pressed(self):
                self.pgn_stop = True
        def fics_pressed(self):
            loginFrame = LoginDialog(self.parent,self)
            self.parent.wait_window(loginFrame.LoginFrame)
            networkDialog = NetworkInterfaceDialog(self.parent,self.network_player)
                                
                        
                                                        
                        
if __name__ == "__main__":
        tstEngine =  ChessEnginePlayer()
        tstEngine.set_board(chess.Board())
        pathEngine="/usr/local/bin/stockfish"
        tstEngine.set_engine_path(pathEngine)
        root = Tk()
        root.wm_title("Sandman Chess v 0.1 ")
        root.resizable(0,0)
        ui = SandmanGui(root)
        testTheme = GuiTheme("./themes/boring")
        print(testTheme.get_themes("./themes"))        
        ui.set_theme("boring",False)
        ui.init_board(root)
        ui.draw_main_board()
        print(  ui.chessBoard)
        root.mainloop()
