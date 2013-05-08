Read several "journal" files and output a merged version.

These "journal" files are files that I write as, well, a journal. They
are simple text files that follow the format:

01 May 2013
-----------

Bla bla bla

Etc


07 May 2013
-----------

Even more bla bla bla.


I write them in different machines, and so it is convenient to have
this program to merge them form time to time.

In my .emacs I have defined:

(defun insert-current-date ()
  (interactive)
  (let ((date (format-time-string "%d %B %Y")))
    (insert "\n\n" date "\n"
            (make-string (length date) ?-) "\n\n")))

(global-set-key (kbd "C-c C-d") 'insert-current-date)

So I start my sessions by opening the journal file and pressing
"Ctrl-c Ctrl-d" to have the current date inserted and start writing.
