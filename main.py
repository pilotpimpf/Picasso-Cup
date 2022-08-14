from igcLib import igcfile
import sys
import os

def name():
    pass

def noname():
    filepath = sys.argv[1]
    outputfolder = filepath.split("/")[1]
    if not os.path.exists(f"output/{outputfolder}/"):
        os.mkdir(f"output/{outputfolder}/")

    files = [os.path.join(sys.path[0], filepath, f) for f in os.listdir( os.path.join(sys.path[0], filepath))]
    for fp in files:
        flight = igcfile(fp)
        newname = flight.rename()

        with open(fp, "r") as f:
            content = f.read()

        with open(f"output/{outputfolder}/{newname}.igc", "w") as f:
            f.write(content)

        flight.generate_html(f"output/{outputfolder}/{newname}.html")

def main():
    if len(sys.argv) == 2: noname()
    elif len(sys.argv) == 3: name()

    if os.path.exists("tmp.json"): os.remove("tmp.json")


if __name__ == "__main__":
    main()