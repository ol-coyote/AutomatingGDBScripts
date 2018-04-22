# -----------------------------------------------------------------------
# This is an example illustrating how to use customview in Python
# (c) Hex-Rays
#
import idaapi
import idc
from idaapi import simplecustviewer_t

# -----------------------------------------------------------------------
class say_something_handler_t(idaapi.action_handler_t):
    def __init__(self, thing):
        idaapi.action_handler_t.__init__(self)
        self.thing = thing

    def activate(self, ctx):
        print self.thing

    def update(self, ctx):
        return idaapi.AST_ENABLE_ALWAYS


# -----------------------------------------------------------------------
class mycv_t(simplecustviewer_t):
    def Create(self, sn=None):
        # Form the title
        title = "Stack Dump View"
        if sn:
            title += " %d" % sn

        # Create the customviewer
        if not simplecustviewer_t.Create(self, title):
            return False
        with open('C:/Users/workshopadmin/Desktop/vm_share/dumptxt/stackdump2018.04.19-01.29.41.log','r') as f:
            output=f.readlines()
        for i in output:
            self.AddLine(i)
        '''
        for i in xrange(0, 100):
            fg, bg = idaapi.COLOR_PREFIX, None
            # make every 10th line a bit special
            if i % 10 == 0:
                fg = idaapi.COLOR_DEFAULT # i.e., white...
                bg = 0xFFFF00             # ...on cyan
            pfx = idaapi.COLSTR("%3d" % i, idaapi.SCOLOR_PREFIX)
            self.AddLine("%s: Line %d" % (pfx, i), fgcolor=fg, bgcolor=bg)
        '''
        return True

    def OnClick(self, shift):
        """
        User clicked in the view
        @param shift: Shift flag
        @return: Boolean. True if you handled the event
        """
        print "OnClick, shift=%d" % shift
        return True

    def OnDblClick(self, shift):
        """
        User dbl-clicked in the view
        @param shift: Shift flag
        @return: Boolean. True if you handled the event
        """
        word = self.GetCurrentWord()
        if not word: word = "0xDEADBEEF"
        print "OnDblClick, shift=%d, current word=%s" % (shift, word)
        if ":" in word:
            word = word.split(":")[0]
        idc.Jump(int(word,16))
        return True

    def OnCursorPosChanged(self):
        """
        Cursor position changed.
        @return: Nothing
        """
        print "OnCurposChanged"

    def OnClose(self):
        """
        The view is closing. Use this event to cleanup.
        @return: Nothing
        """
        print "OnClose " + self.title

    def OnKeydown(self, vkey, shift):
        """
        User pressed a key
        @param vkey: Virtual key code
        @param shift: Shift flag
        @return: Boolean. True if you handled the event
        """
        print "OnKeydown, vk=%d shift=%d" % (vkey, shift)
        # ESCAPE?
        if vkey == 27:
            self.Close()
        # VK_DELETE
        elif vkey == 46:
            n = self.GetLineNo()
            if n is not None:
                self.DelLine(n)
                self.Refresh()
                print "Deleted line %d" % n
        # Goto?
        elif vkey == ord('G'):
            n = self.GetLineNo()
            if n is not None:
                v = idaapi.ask_long(self.GetLineNo(), "Where to go?")
                if v:
                    self.Jump(v, 0, 5)
        elif vkey == ord('R'):
            print "refreshing...."
            self.Refresh()
        elif vkey == ord('C'):
            print "refreshing current line..."
            self.RefreshCurrent()
        elif vkey == ord('A'):
            s = idaapi.ask_str("NewLine%d" % self.Count(), 0, "Append new line")
            self.AddLine(s)
            self.Refresh()
        elif vkey == ord('X'):
            print "Clearing all lines"
            self.ClearLines()
            self.Refresh()
        elif vkey == ord('I'):
            n = self.GetLineNo()
            s = idaapi.ask_str("InsertedLine%d" % n, 0, "Insert new line")
            self.InsertLine(n, s)
            self.Refresh()
        elif vkey == ord('E'):
            l = self.GetCurrentLine(notags=1)
            if not l:
                return False
            n = self.GetLineNo()
            print "curline=<%s>" % l
            l = l + idaapi.COLSTR("*", idaapi.SCOLOR_VOIDOP)
            self.EditLine(n, l)
            self.RefreshCurrent()
            print "Edited line %d" % n
        else:
            return False
        return True

    def OnHint(self, lineno):
        """
        Hint requested for the given line number.
        @param lineno: The line number (zero based)
        @return:
            - tuple(number of important lines, hint string)
            - None: if no hint available
        """
        return (1, "OnHint, line=%d" % lineno)

# -----------------------------------------------------------------------
try:
    # created already?
    mycv
    print "Already created, will close it..."
    mycv.Close()
    del mycv
except:
    pass

def show_win():
    x = mycv_t()
    if not x.Create():
        print "Failed to create!"
        return None
    x.Show()
    tcc = x.GetWidget()

    # Register actions
    for thing in ["Hello", "World"]:
        actname = "custview:say_%s" % thing
        idaapi.register_action(
            idaapi.action_desc_t(actname, "Say %s" % thing, say_something_handler_t(thing)))
        idaapi.attach_action_to_popup(tcc, None, actname)
    return x

mycv = show_win()
if not mycv:
    del mycv

def make_many(n):
    L = []
    for i in xrange(1, n+1):
        v = mycv_t()
        if not v.Create(i):
            break
        v.Show()
        L.append(v)
    return L