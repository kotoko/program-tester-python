APP=program-tester
ROOT_DIRECTORY=.
PO_FILES=$(wildcard $(ROOT_DIRECTORY)/l10n/*/LC_MESSAGES/$(APP).po)
MO_FILES=$(PO_FILES:%.po=%.mo)


all: translation

translation: $(MO_FILES)

%.mo: %.po
	msgfmt $< -o $@

clean:
	rm -f $(MO_FILES)


.PHONY: all clean translation
