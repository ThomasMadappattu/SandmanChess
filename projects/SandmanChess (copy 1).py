import Tkinter
from Tkinter import *
import chess
import chess.uci
import os
import random
import telnetlib
import tkFileDialog
import tkMessageBox

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
                

class NetWorkPlayer:
        def __init__(self):
                self.Constants = UIConstants()
                
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
        def __init__(self):
                self.rows = 8 
                self.columns = 8 
                self.colorWhite = "#DDB88C"
                self.colorBlack = "#A66D4F"
                self.totalSquares = 64
                self.squareLen = 70
                self.chessBoard = chess.Board()
                self.adjust =  self.squareLen/2
                self.clickedBoard   = 0
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
                self.themeDir='./themes'
                self.theme = None
                
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
                self.networkMenu  =  Menu ( self.parent )
                self.menubar.add_cascade ( label = "Network", menu = self.networkMenu)
                self.trainingMenu  =  Menu (self.parent)
                self.menubar.add_cascade ( label = "Training", menu = self.trainingMenu)
                self.pgnMenu  =  Menu ( self.parent)
                self.menubar.add_cascade ( label = "PGN", menu = self.pgnMenu )
                self.canvas = Canvas ( self.parent, width = self.rows * self.squareLen, height = self.columns * self.squareLen, background = "grey")
                self.canvas.pack(padx = 8,pady= 8)
                self.lblNotifications = Label(text = "Notification", anchor="w")
                self.txtPgn           = Text( self.parent, height=10)
                self.draw_main_board()
                self.parent.config( menu = self.menubar)
                self.lblNotifications.pack()
                self.txtPgn.pack()
                self.canvas.bind("<ButtonRelease-1>", self.board_clicked)
                
        def menu_flip_board(self):
                self.flip_board()
                self.draw_main_board()
                
        def canvas_click_toggle(self):
                if ( self.clickedBoard == 0 ):
                        self.clickedBoard = 1
                else:
                        self.clickedBoard = 0

        def board_clicked( self,event):
                posx = event.x
                posy = event.y
                row = posx / self.squareLen
                col = posy /self.squareLen
                startx = row * self.squareLen
                starty = col * self.squareLen
                endx = startx + self.squareLen
                endy = starty + self.squareLen
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
                
        def set_theme(self,theme):
                self.theme = theme
                
        def set_player(self, playerType):
                self.player = playerType

        def flip_board(self):
                if (self.flip):
                        self.flip = False
                else:
                        self.flip = True
                

        
        
                                        
                        
if __name__ == "__main__":
        tstEngine =  ChessEnginePlayer()
        tstEngine.set_board(chess.Board())
        pathEngine="/usr/local/bin/stockfish"
        tstEngine.set_engine_path(pathEngine)
        root = Tk()
        root.wm_title("Sandman Chess v 0.1 ")
        root.resizable(0,0)
        ui = SandmanGui()
        testTheme = GuiTheme("./themes/boring")
        print(testTheme.get_themes("./themes"))        
        ui.set_theme(testTheme)
        ui.init_board(root)
        ui.draw_main_board()
        print(  ui.chessBoard)
        root.mainloop()
