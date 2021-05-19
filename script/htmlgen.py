r"""
    Generate Static HTML required to post on github
"""

from os import listdir,remove,path
import argparse

front_matter = r"""
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<!-- Automaticaly generated content, please update scripts/htmlgen.py for any change -->
   <head>
      <meta charset="UTF-8">
      <title align="center">multilingual-tts samples"</title>
      <style type="text/css">
        body, input, select, td, li, div, textarea, p {
        	font-size: 11px;
        	line-height: 16px;
        	font-family: verdana, arial, sans-serif;
        }

        body {
        	margin:5px;
        	background-color:white;
        }

        h1 {
        	font-size:16px;
        	font-weight:bold;
        }

        h2 {
        	font-size:14px;
        	font-weight:bold;
        }
      </style>
   </head>
   <body>
      <article>
         <header>
            <h1>Improving Polyglot Speech Synthesis through Multi-task and Adversarial Learning</h1>
         </header>
      </article>


      <div>
        <h2>Abstract</h2>
        <p>It is still quite challenging for polyglot speech synthesis systems to synthesise speech with the same pronunciations and accent as a native speaker, especially when there are fewer speakers per language. In this work, we target an extreme version of the polyglot synthesis problem, where we have only one speaker per language, and the system has to learn to disentangle speaker from language features from just one speaker-language pair. To tackle this problem, we propose a novel approach based on a combination of multi-task learning and adversarial learning to help the model produce more realistic acoustic features for speaker-language combinations for which we have no data. Our proposed system improves the overall naturalness of synthesised speech achieving upto 4.2% higher naturalness over a multispeaker baseline. Our qualitative listening tests also demonstrate that system produces speech which sounds less accented and more natural to a native speaker.</p>
      </div>

      <h2> Supplementary audio samples </h2>
"""

back_matter = r"""
   </body>
</html>
"""


def get_row_column(root='./Long'):
    Columns = [x for x in listdir(root) if x[0] != '.']
    assert len(Columns) > 0, f"No subfolders under {root}/"
    Rows = set(listdir(f"{root}/{Columns[0]}"))
    for c in Columns:
        Rows = Rows.intersection(set(listdir(f"{root}/{c}")))

    cleanup(root,Rows,Columns)

    return list(Rows), Columns

def cleanup(root,rows,columns):
    for c in columns:
        for r in listdir(f"{root}/{c}"):
            if r not in rows:
                fpath = f"{root}/{c}/{r}"
                if args.delete:
                    assert path.isfile(fpath),f"{fpath} not single file"
                    remove(fpath)
                else:
                    print(f"would delete {fpath}")

def gen_table_header(name='noname', cols=["nothing"], file=None):
    print(f"""
    <div>
    <h2> {name} </h2>
      <table border = "1" class="inlineTable">
    """, file=file)
    print(
        ''.join([r"""
        <col width="300">""" for _ in cols]),
        file=file)
    print(
        """     <tr> """, file=file)
    print(
        ''.join([f"""
        <th>{col}</th>""" for col in cols]) +
        """
</tr>""", file=file)


def audio_entry(audio, file=None):
    print(
        f"""
    <td>
        <audio controls style="width: 200px;">
        <source src={audio} type="audio/wav">
            Your browser does not support the audio element.
        </audio>
    </td>""", file=file)


def text_entry(text, file=None):
    print(
        f"""
        <th>{text}</th>""",
        file=file)


def single_row(columns, text=True, file=None):
    print("<tr>", file=file)
    for c in columns:
        if(text):
            text_entry(c, file=file)
        else:
            audio_entry(c, file=file)
    print("</tr>", file=file)


def gen_table(args, file=None):
    for table in args.table:
        if isinstance(table,list):
            t = table[0]
        else:
            t = table
        rows, cols = get_row_column(root=f"./samples/{t}")
        cols=['Single_Spk','Multi_Spk','Multi_Spk_with_MT+GAN']
        gen_table_header(name=t, cols=cols, file=file)
        cols=['Single_Spk','Multi_Spk','Multi_Spk_with_MT+GAN']
        for r in rows:
            c = [f"./samples/{t}/{x}/{r}" for x in cols]
            single_row(c, text=args.name_only, file=file)
        print("""
            </table>
        </div>
        """, file=file)


def main(args):
    fname = args.output
    with open(fname, 'w') as f:
        print(front_matter, file=f)
        gen_table(args, file=f)
        print(back_matter, file=f)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-o', '--output', type=str,
                        default='index.html', help='output name')
    parser.add_argument('-n', '--name_only',
                        action="store_true", help='put file names only')
    parser.add_argument('-t', '--table', type=str, action="append",
                        nargs='+', help='names of tables', default=['English','French','German','Italian','Spanish'])
    parser.add_argument('-del', '--delete',
                        action="store_true", help='delete files')


    global args
    args = parser.parse_args()

    main(args)
