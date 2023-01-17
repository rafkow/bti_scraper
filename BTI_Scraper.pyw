from tkinter import Radiobutton, StringVar, Tk, messagebox, Frame, Button, Label, Entry
from tkinter.constants import HORIZONTAL
from tkinter.ttk import Progressbar
from ec_europa import get_bti
import threading


class MainWindow(Frame):
    
    FONT = "Bell_MT 11"

    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.grid()
        self.createWidgets()
        self.thread = None
    
    def createWidgets(self):
        self.searchResultsLabel()
        self.linkEntry()
        self.instructionButton()
        self.radioButton()
        self.progressbar()
        self.progressInfo()
        self.collectButton()
        self.exitButton()
        self.authorLabel()
    
    def searchResultsLabel(self):
        Label(self, text="Link to search results:", font=self.FONT).grid(column=0, row=0)

    def linkEntry(self):
        self.entryLink = Entry(self, width=50)
        self.entryLink.grid(column=1, row=0, columnspan=2, pady=15)

    def instructionButton(self):
        self.buttonInstruction = Button(self, text="Instructions", command=self.showInstruction, font=self.FONT)
        self.buttonInstruction.grid(column=3, row=0)
    def showInstruction(self):
        message = "1. Go to the BTI database site 'https://ec.europa.eu/taxation_customs/dds2/ebti/ebti_consultation.jsp?Lang=en' and make your search. \n"
        message += "2. Copy link to the page when the search is complete. \n"
        message += "3. Paste link to this program and hit 'Collect' button. \n"
        message += "4. Collected data will be saved as csv file in same folder as BTI Scraper. \n\n"
        message += "Program can retrieve basic BTI data (BTI number, HTS code, start/end date of validity, number of images) or full BTI data - BTI'S with description and classification justification. \n"
        message += "If you have any questions or any problems with application contact the author: bszmyt@livingstonintl.com"
        message += "\n If the program does not work try connecting to VPN and restart computer. Another reason may be the antivirus, which blocked this program."
        message += "\n If above solution fail, try updating chromedriver.exe or just try running the program again. If everything of this fail, the only solution may be debugging in the program code."
        messagebox.showinfo("Instructions", message=message, parent=self.master)
    
    def radioButton(self):
        self.dataAmountchoice = StringVar(value="basic")
        dataAmountbasic = Radiobutton(self, text="Basic data", variable=self.dataAmountchoice, value="basic")      
        dataAmountfull = Radiobutton(self, text="Full data", variable=self.dataAmountchoice, value="full")
        dataAmountbasic.grid(column=1, row=1)
        dataAmountfull.grid(column=2, row=1)

    def progressbar(self):
        self.bar = Progressbar(self, orient=HORIZONTAL, length=450)
        self.bar.grid(column=0, row=2, columnspan=4, padx=80, pady=6)
    
    def progressInfo(self):
        self.infoLabel = Label(self, text="Waiting for link...", width=50, font=self.FONT)
        self.infoLabel.grid(column=0, row=3,columnspan=4)

    def exitButton(self):
        self.buttonExit = Button(self, text="Exit", command=self.master.destroy, font=self.FONT, width=10)
        self.buttonExit.grid(column=2, row=4, pady=6, padx=60)

    def authorLabel(self):
        Label(self, text="Author: Bartosz Szmyt, refactor: Oliwia Drangowska", font="Arial 8").grid(column=0, row=5, columnspan=2)

#############################################################################################################################################################################
    def collectButton(self):
        self.collectButton = Button(self, text="Collect",
                                    command=self.start_download,
                                    font=self.FONT, width=10)

        self.collectButton.grid(column=1, row=4)



    def start_download(self):
        full_report = 1 if self.dataAmountchoice.get() == "full" else 0
        url = self.entryLink.get()
        if url:
            self.thread = threading.Thread(target=get_bti, args=(url, full_report, self))
            self.thread.start()


    def checkifThumbnail(self, btiLink):
        """Return True when user provided link in thumbnail view"""
        if "viewVal=Thumbnail" in btiLink:
            messagebox.showinfo("Information", "Your search results are in thubnail-view mode. Please change to list view and try again.")
            return True
        else:
            return False


    def endProcess(self, Browser=False):
        """Reset program state after error \n
           If "Browser" object provided, then function will close browser driver"""
        if Browser:
            Browser.CloseDriver()
        messagebox.showerror("Error!","There's a problem with link or searching browser! Check if link leads to the BTI search page... If it's correct try running programm again. Otherwise contact administrator.")
        self.updateBar(barValue=0, message="Waiting for link...")
        self.entryLink.delete(0,"end")

    def processCompleted(self):
        """Stuff after successfully ended process"""
        self.updateBar(barValue=100, message="Data saved")
        self.entryLink.delete(0,"end")
        messagebox.showinfo("Completed","Data collection complete.", parent=self.master)
        self.updateBar(barValue=0, message="Waiting for link...")

    def basicSearch(self, Browser):
        while Browser.NextButtonExist:
            Browser.GetRows()
            Browser.ClickNextButton()
            self.update_idletasks()
    
    def deepSearch(self, Browser, BTInumbers):
        for number in BTInumbers:
            Browser.openBTIsite(number)
            Browser.getFulldata()
    

def start():
    root = Tk()
    mainWindow = MainWindow(root)
    root.title("BTI Scraper")
    root.resizable(width=False, height=False)
    root.mainloop()


if __name__ == "__main__":
    start()


