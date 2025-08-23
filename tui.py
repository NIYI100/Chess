try:
	import curses
except ModuleNotFoundError:
	print("This TUI requires curses. On Windows, install with: pip install windows-curses")
	raise
from typing import Optional, Set, Tuple

from Board.board import Board
from Board.constants import BOARD_SIZE, FILES_LABELS, RANKS_LABELS, EMPTY
from MoveGeneration.move_generation import calculate_legal_moves
from Engine.board_evalation import evaluate
from Engine.engine import get_best_move


Square = Tuple[int, int]  # (rank, file), rank 0 at top (8th), file 0 at left (a)

CELL_W = 3
BOARD_TOP = 2
BOARD_LEFT = 4

ENGINE_SEARCH_DEPTH = 3


def init_colors():
	curses.start_color()
	curses.use_default_colors()
	curses.init_pair(1, curses.COLOR_WHITE, -1)     # normal
	curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_YELLOW)  # cursor
	curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_CYAN)    # selected
	curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_GREEN)   # move (empty target)
	curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_RED)     # capture target


def is_enter(key: int) -> bool:
	return key in (curses.KEY_ENTER, 10, 13)


def addstr_safe(stdscr, y: int, x: int, text: str, attr=0):
	try:
		stdscr.addstr(y, x, text, attr)
	except curses.error:
		pass


def draw_labels(stdscr):
	# file labels on top and bottom
	top = "  " + "".join(f"{f:^{CELL_W}}" for f in FILES_LABELS)
	addstr_safe(stdscr, 0, BOARD_LEFT, top, curses.color_pair(1))
	addstr_safe(stdscr, BOARD_TOP + BOARD_SIZE, BOARD_LEFT, top, curses.color_pair(1))

	# rank labels on left side
	for r in range(BOARD_SIZE):
		addstr_safe(stdscr, BOARD_TOP + r, 0, f"{RANKS_LABELS[r]:>2}", curses.color_pair(1))


def draw_board(stdscr, board: Board, cursor: Square, selected: Optional[Square], move_targets: Set[Square], turn: str, engine_info: Optional[str] = None):
	for r in range(BOARD_SIZE):
		for f in range(BOARD_SIZE):
			y = BOARD_TOP + r
			x = BOARD_LEFT + f * CELL_W
			piece = board.board[r][f]
			ch = piece if piece != EMPTY else ' '

			attr = curses.color_pair(1)
			if selected == (r, f):
				attr = curses.color_pair(3)
			elif (r, f) in move_targets:
				# show 'x' on empty, red bg on capture
				if piece == EMPTY:
					ch = 'x'
					attr = curses.color_pair(4)
				else:
					attr = curses.color_pair(5)

			if cursor == (r, f):
				# cursor overrides only background if no selection/move overlay
				if selected != (r, f) and (r, f) not in move_targets:
					attr = curses.color_pair(2)

			addstr_safe(stdscr, y, x, f" {ch} ", attr)

	# evaluation line (from active side's perspective)
	score = evaluate(board, turn)
	addstr_safe(stdscr, BOARD_TOP + BOARD_SIZE + 1, 0, f"Eval ({turn}): {score/100:+.2f}", curses.color_pair(1))

	# last engine info line (if any)
	if engine_info:
		addstr_safe(stdscr, BOARD_TOP + BOARD_SIZE + 2, 0, engine_info, curses.color_pair(1))

	# info line
	addstr_safe(stdscr, BOARD_TOP + BOARD_SIZE + 3, 0, f"Turn: {turn}    Arrows: move cursor   Enter/Space: select/move   Esc: cancel   Q: quit", curses.color_pair(1))


 


def screen_to_square(y: int, x: int) -> Optional[Square]:
	r = y - BOARD_TOP
	if r < 0 or r >= BOARD_SIZE:
		return None
	col = x - BOARD_LEFT
	if col < 0:
		return None
	f = col // CELL_W
	if f < 0 or f >= BOARD_SIZE:
		return None
	return (r, f)


def can_select(board: Board, turn: str, sq: Square) -> bool:
	r, f = sq
	p = board.board[r][f]
	if p == EMPTY:
		return False
	return (p.isupper() and turn == 'white') or (p.islower() and turn == 'black')


def _format_move(move: Tuple[Square, Square]) -> str:
	(frm, to) = move
	fr, ff = frm
	tr, tf = to
	return f"{FILES_LABELS[ff]}{RANKS_LABELS[fr]}{FILES_LABELS[tf]}{RANKS_LABELS[tr]}"


def main(stdscr):
	try:
		curses.curs_set(0)
	except curses.error:
		pass
	stdscr.nodelay(False)
	stdscr.keypad(True)

	try:
		init_colors()
	except curses.error:
		pass  # continue without colors if unsupported

	# enable mouse if available
	try:
		curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)
	except curses.error:
		pass

	board = Board()
	turn = 'white'
	cursor: Square = (6, 4)  # start near white king
	selected: Optional[Square] = None
	move_targets: Set[Square] = set()
	last_engine_info: Optional[str] = None

	while True:
		stdscr.clear()
		draw_labels(stdscr)
		draw_board(stdscr, board, cursor, selected, move_targets, turn, last_engine_info)
		stdscr.refresh()

		key = stdscr.getch()

		# Mouse click handling (left click)
		if key == curses.KEY_MOUSE:
			try:
				_, mx, my, _, bstate = curses.getmouse()
				if bstate & curses.BUTTON1_PRESSED or bstate & curses.BUTTON1_CLICKED:
					sq = screen_to_square(my, mx)
					if sq is not None:
						cursor = sq
						# treat as click -> same as Enter
						if selected is None:
							if can_select(board, turn, cursor):
								selected = cursor
								moves, captures = calculate_legal_moves(board, selected)
								move_targets = {to for (_frm, to) in (captures + moves)}
							else:
								selected = None
								move_targets.clear()
						else:
							if cursor in move_targets:
								fr, ff = selected
								tr, tf = cursor
								board.make_move(fr, ff, tr, tf)
								selected = None
								move_targets.clear()
								turn = 'black' if turn == 'white' else 'white'
								if turn == 'black':
									best_score, best_move = get_best_move(board, ENGINE_SEARCH_DEPTH, 'black')
									if best_move is not None:
										(fr2, ff2), (tr2, tf2) = best_move
										board.make_move(fr2, ff2, tr2, tf2)
										turn = 'white'
									else:
										print("Engine (black): no legal moves")
							else:
								# reselect if clicking on own piece; otherwise cancel
								if can_select(board, turn, cursor):
									selected = cursor
									moves, captures = calculate_legal_moves(board, selected)
									move_targets = {to for (_frm, to) in (captures + moves)}
								else:
									selected = None
									move_targets.clear()
				continue
			except curses.error:
				pass  # ignore mouse errors

		# Keyboard handling
		if key in (ord('q'), ord('Q')):
			return
		if key in (27,):  # Esc cancels selection
			selected = None
			move_targets.clear()
			continue
		if key in (curses.KEY_UP, ord('k')):
			cursor = (max(0, cursor[0] - 1), cursor[1])
			continue
		if key in (curses.KEY_DOWN, ord('j')):
			cursor = (min(BOARD_SIZE - 1, cursor[0] + 1), cursor[1])
			continue
		if key in (curses.KEY_LEFT, ord('h')):
			cursor = (cursor[0], max(0, cursor[1] - 1))
			continue
		if key in (curses.KEY_RIGHT, ord('l')):
			cursor = (cursor[0], min(BOARD_SIZE - 1, cursor[1] + 1))
			continue
		if is_enter(key) or key == ord(' '):
			if selected is None:
				if can_select(board, turn, cursor):
					selected = cursor
					moves, captures = calculate_legal_moves(board, selected)
					move_targets = {to for (_frm, to) in (captures + moves)}
				else:
					selected = None
					move_targets.clear()
			else:
				if cursor in move_targets:
					fr, ff = selected
					tr, tf = cursor
					board.make_move(fr, ff, tr, tf)
					selected = None
					move_targets.clear()
					turn = 'black' if turn == 'white' else 'white'
					if turn == 'black':
						best_move, best_score, used_tt = get_best_move(board, ENGINE_SEARCH_DEPTH, 'black')
						if best_move is not None:
							(fr2, ff2), (tr2, tf2) = best_move
							board.make_move(fr2, ff2, tr2, tf2)
							last_engine_info = f"Engine (black): {_format_move(best_move)}  Eval: {best_score/100:+.2f}  TT: {'yes' if used_tt else 'no'}"
							print(last_engine_info)
							turn = 'white'
						else:
							print("Engine (black): no legal moves")
				else:
					# reselect if on own piece, otherwise cancel
					if can_select(board, turn, cursor):
						selected = cursor
						moves, captures = calculate_legal_moves(board, selected)
						move_targets = {to for (_frm, to) in (captures + moves)}
					else:
						selected = None
						move_targets.clear()


if __name__ == "__main__":
	curses.wrapper(main)