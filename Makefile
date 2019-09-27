clean:
	rm -f output*.xlsx
test:
	python3 cyberark.py cyberark_mike_safe_v1.xlsx
