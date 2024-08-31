#!/usr/bin/env python3
import os
from datetime import date, timedelta
from typing import Generator


def all_sundays(year: int) -> Generator[date, None, None]:
  day = date(year, 9, 1)
  day += timedelta(days = 6 - day.weekday())
  while not (day.year == year + 1 and day.month == 9):
    yield day
    day += timedelta(days = 7)


class Object(object):
  pass

NullTag = Object()
NullTag.indent = -2


class Tag:
  def __init__(self, preTag, file, parens):
    self.indent = preTag.indent + 2
    self.file = file
    self.begin, self.end = parens

  def __enter__(self):
    self.file.write(self.indent * ' ' + self.begin + '\n')
    return self

  def __exit__(self, type, value, traceback):
    self.file.write(self.indent * ' ' + self.end + '\n')


def append_preamble(file):
  # step n: write document preamble
  file.write('\\documentclass{article}\n')
  file.write('\\usepackage[default]{lato}')
  file.write('\\usepackage[T2A]{fontenc}\n')
  file.write('\\usepackage[utf8x]{inputenc}\n')
  file.write('\\usepackage[english, russian]{babel}\n')
  file.write('\\usepackage{wasysym}\n')
  file.write('\\usepackage{vmargin}\n')
  file.write('\\setmarginsrb{1cm}{0.2cm}{0.2cm}{0.2cm}{0pt}{0pt}{0pt}{0mm}\n')
  file.write('\\setpapersize{A4}\n')
  file.write('\\usepackage{booktabs}\n')
  file.write('\\renewcommand\\arraystretch{2}\n')
  file.write('\\pagestyle{empty}\n')
  file.write('\\setlength{\\tabcolsep}{30pt}\n')
  file.write('\\renewcommand{\\arraystretch}{0.65}\n')
  file.write('\\sloppy\n')


current_year = date.today().year
janitors = os.getenv('JANITORS', '').split(',')


begin = lambda name: '\\begin{' + name + '}'
end = lambda name: '\\end{' + name + '}'
parens = lambda name: ( begin( name ), end( name ) )


def append_indent_line(tag: Tag, file, content: str):
  file.write((tag.indent + 2) * ' ' + content + '\n')


def main():
  global_file = 'data.tex'
  with open(global_file, 'w', encoding = 'utf-8') as f:
    append_preamble(f)

    with Tag(NullTag, f, parens('document')) as DocumentTag:
      append_indent_line(DocumentTag, f, '\\section*{\\centerline{ График уборки }}')
      append_indent_line(DocumentTag, f, '\\paragraph*{\\centerline{ Ванна, раковина, зеркало, пол в ванной, туалет, мусорка, пол в туалете, пол в блоке } }\\mbox{}\\\\')

      with Tag(DocumentTag, f, (begin('table') + '[!ht]', end('table'))) as TableTag:
        append_indent_line(TableTag, f, '\\small')
        append_indent_line(TableTag, f, '\\centering')

        with Tag(TableTag, f, (begin('tabular') + '{' + ('|'.join(['l' for i in range(len(janitors) + 1)])) + '}', end('tabular'))) as TabularTag:
          append_indent_line(TabularTag, f, '\\toprule')
          columns = ['Дата'] + janitors
          append_indent_line(TabularTag, f, ' & '.join(columns))

          for idx, day in enumerate(all_sundays(current_year)):
            append_indent_line(TabularTag, f, '\\\\\\midrule')
            marks = ['           '] * (len(janitors) - 1)
            marks.insert(idx % len( janitors ), '{ \\large $ \\Box $ }')
            append_indent_line(TabularTag, f, str(day.day).zfill(2) + '.' + str(day.month).zfill(2) + ' & ' + ' & '.join(marks))

          append_indent_line(TabularTag, f, '\\\\\\bottomrule')


if __name__ == '__main__':
  main()
