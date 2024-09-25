# Wiki
Check the [Wiki](https://github.com/HobbitDur/pandemona/wiki) for info detail

# How to use
@segachief instruction:
1) Replace the default files within InputFiles with your modded versions of those files (m000.bin, m000.msg, etc.) and then run the Pandemona.exe. You can get the m000.bin, etc. by using an archive tool such as Deling from the game's files.

You will only see an empty CMD window pop up briefly, there is no immediate visual feedback on the processes being undertaken; there is no GUI or editor interface, this step just produces the files that we will modify ourselves in a text editor.

2) The PandemonaFiles folder will now contain files with .pandemona; open these in Notepad++ or similar and edit them.

The Resources folder contains all IDs and item names for reference; refer to these when making changes within the pandemona files.

You can edit the text, values, and other information within these files but try to keep it the same structure so that the tool can read it, and keep the length of your edited text within reasonable limits.

Bear in mind that the game uses some special text characters to save space (for instance, 'into' will appear as '\ninto', try to preserve
these specially formatted characters if you can but I don't think it's critical to do so). <i>HobbitDur note: \n means "Return to line", if you remove it the text will appear on a single line</i>

3) Once the edits are complete, run Pandemona.exe again. This will convert the .pandemona files into usable game files within the
Output folder. The .bin files are data, the .msg files are the text. Insert them back into the game using Deling or a similar archive manager.

The tool's general workflow is: Read InputFiles, produce 'Pandemona' files (to be edited in a text editor), create OutputFiles from the pandemona files.
