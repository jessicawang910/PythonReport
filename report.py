#import time
import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
c = canvas.Canvas("form.pdf")
c.setLineWidth(.5)
c.setFont("Helvetica", 12)

c.drawString(100,750,"Zhuzhu's Report Template")
#formatted_time = time.ctime()
formatted_time = datetime.date.today().strftime("%m/%d/%Y")
c.drawString(450,750, formatted_time)
c.line(50,735,550,735)
c.save()

def make_note(parameters):
    """Builds a pdf note based on the passed dictionary of parameters.
    For the structure of the parameters, see the code of the function
    make_example_note.
    """
    story = [ ]
    story.append(Paragraph("Project status note" , h1))
    story.append(Paragraph("SciLifeLab Stockholm" , h2))
    story.append(Paragraph("{:%B %d, %Y}".format(datetime.now()) , h2))

    for headline , paragraph in paragraphs.items():
        story.append(Paragraph(headline , h3))
        if isinstance(paragraph , dict):
            for sub_headline , sub_paragraph in paragraph.items():
                story.append(Paragraph(sub_headline , h4))
                story.append(Paragraph(sub_paragraph , p))
        else:
            try:
                story.append(Paragraph(paragraph.format(**parameters) , p))
            except:
                print "Failed to make note. Value of parameters: " , parameters
                sys.exit(0)
        if headline == 'Samples':
            data = parameters[ 'sample_table' ]
            t = Table(data , 5 * [ 1.25 * inch ] , len(data) * [ 0.25 * inch ])
            t.setStyle(TableStyle([ ('ALIGN' , (1 , 1) , (-2 , -2) , 'RIGHT') ,
                                    ('VALIGN' , (0 , 0) , (0 , -1) , 'TOP') ,
                                    ('ALIGN' , (0 , -1) , (-1 , -1) , 'CENTER') ,
                                    ('VALIGN' , (0 , -1) , (-1 , -1) , 'MIDDLE') ,
                                    ('INNERGRID' , (0 , 0) , (-1 , -1) , 0.25 , colors.black) ,
                                    ('BOX' , (0 , 0) , (-1 , -1) , 0.25 , colors.black) ,
                                    ]))
            story.append(t)

    doc = SimpleDocTemplate("{project_name}_status_note.pdf".format(**parameters))
    doc.build(story , onFirstPage=formatted_page , onLaterPages=formatted_page)