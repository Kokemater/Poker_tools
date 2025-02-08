

def calculate_pot_odds(pot_size, call_size):
	return (call_size/(pot_size + call_size))

pot_size = int(input("Pot size: "))
call_size = int(input("Call size: "))

equity_necessary = calculate_pot_odds(pot_size, call_size)

print(f"Call if your equity > {equity_necessary*100}%")
