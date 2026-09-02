from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, KeepTogether

output = "docs/quest8-10-presentation-guide.pdf"
doc = SimpleDocTemplate(
    output,
    pagesize=letter,
    rightMargin=0.65 * inch,
    leftMargin=0.65 * inch,
    topMargin=0.55 * inch,
    bottomMargin=0.55 * inch,
)

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(
    name="CoverTitle", parent=styles["Title"], alignment=TA_CENTER,
    fontSize=25, leading=30, textColor="#17324D", spaceAfter=14,
))
styles.add(ParagraphStyle(
    name="CoverSub", parent=styles["Normal"], alignment=TA_CENTER,
    fontSize=13, leading=18, textColor="#52606D", spaceAfter=24,
))
styles.add(ParagraphStyle(
    name="Section", parent=styles["Heading1"], fontSize=19, leading=23,
    textColor="#0B7285", spaceBefore=5, spaceAfter=9,
))
styles.add(ParagraphStyle(
    name="Sub", parent=styles["Heading2"], fontSize=12.5, leading=16,
    textColor="#17324D", spaceBefore=8, spaceAfter=4,
))
styles.add(ParagraphStyle(
    name="Body", parent=styles["BodyText"], fontSize=10.5, leading=14,
    textColor="#263238", spaceAfter=6,
))
styles.add(ParagraphStyle(
    name="Quote", parent=styles["BodyText"], fontSize=12, leading=17,
    leftIndent=14, rightIndent=10, textColor="#0B7285", spaceBefore=5,
    spaceAfter=8,
))
styles.add(ParagraphStyle(
    name="Flow", parent=styles["BodyText"], fontSize=10.5, leading=16,
    leftIndent=12, textColor="#263238", spaceAfter=6,
))
styles.add(ParagraphStyle(
    name="Small", parent=styles["BodyText"], fontSize=9, leading=12,
    textColor="#52606D", spaceAfter=3,
))

story = []
def p(text, style="Body"):
    story.append(Paragraph(text, styles[style]))
def gap(size=5):
    story.append(Spacer(1, size))
def bullets(items):
    for item in items:
        p("&bull; " + item, "Body")

def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColorRGB(0.32, 0.38, 0.42)
    canvas.drawString(0.65 * inch, 0.3 * inch, "CSE 3320 OS Lab 1 | Quests 8-10")
    canvas.drawRightString(7.85 * inch, 0.3 * inch, f"Page {doc.page}")
    canvas.restoreState()

p("Quests 8-10", "CoverTitle")
p("Simple presentation guide", "CoverSub")
p("The whole story", "Sub")
p("Quest 8 prepares the screen. Quest 9 makes interrupts work. Quest 10 uses interrupts to animate the donut.", "Quote")
p("Presentation goal", "Sub")
p("Explain what each part does, why it is organized that way, and how the parts connect. Use the short answers below instead of reading code line by line.", "Body")
gap(10)
p("Quick map", "Sub")
p("Framebuffer = memory containing pixels", "Flow")
p("Offset = which part of a larger image is visible", "Flow")
p("Interrupt = a signal asking the CPU to handle an event", "Flow")
p("Timer = an alarm that creates an interrupt", "Flow")
p("Animation = draw a frame, set the next alarm, repeat", "Flow")
story.append(PageBreak())

p("Quest 8: Framebuffer Offsets", "Section")
p("What does it do?", "Sub")
p("<b>test_fb_voffset()</b> in <b>unittests.c</b> creates a virtual framebuffer that is twice as wide and twice as tall as the visible screen. It fills the four sections with different colors, then changes the visible section.", "Body")
p("Say it this way", "Sub")
p("A framebuffer is memory that stores screen pixels. The program draws one large picture, but the monitor shows only one part of it. The offset moves the visible window, like moving a camera over a larger picture.", "Quote")
p("Why is it structured this way?", "Sub")
p("Changing the viewport is faster than copying or redrawing the whole screen. This idea can be used for scrolling or switching between images that were already prepared.", "Body")
p("Flow", "Sub")
p("1. Create a large virtual framebuffer.<br/>2. Draw four colored sections.<br/>3. Select offset (0,0), wait, and select the other three offsets.<br/>4. <b>fb_set_voffsets()</b> sends the new offsets through the mailbox to the GPU and checks that they were accepted.", "Flow")
p("What if?", "Sub")
bullets([
    "If the virtual framebuffer is not larger, there is nowhere else to move.",
    "If fb_set_voffsets() is skipped, the screen stays on the first section.",
    "If the framebuffer is not initialized, the program does not know the correct address and layout for drawing.",
])
story.append(PageBreak())

p("Quest 9: System Timer IRQ", "Section")
p("What does it do?", "Sub")
p("An interrupt is a signal that tells the CPU: stop briefly, handle this event, and then continue. The timer acts like an alarm clock.", "Quote")
p("The important pieces", "Sub")
bullets([
    "enable_interrupt_controller(0) allows the timer signal through the hardware controller.",
    "enable_irq() allows the CPU to receive IRQs.",
    "The vector table in entry.S tells the CPU where to go for an IRQ.",
    "kernel_entry saves registers before the handler uses them.",
    "handle_irq() in irq.c identifies the device that caused the interrupt.",
    "kernel_exit restores registers and eret returns to the interrupted code.",
])
p("Flow", "Sub")
p("Timer expires &rarr; CPU receives IRQ &rarr; EL1 IRQ vector &rarr; el1_irq &rarr; handle_irq() &rarr; timer handler &rarr; restore state and return", "Flow")
p("Why does the timer repeat?", "Sub")
p("The timer handler resets the timer after each interrupt. Without that reset, the timer normally fires only once.", "Body")
p("What if?", "Sub")
bullets([
    "If the vector points to the invalid handler, the timer interrupt is treated as an error.",
    "If enable_irq() is missing, the CPU keeps IRQs masked and ignores the interrupt.",
    "If registers are not saved, returning from the interrupt can corrupt the kernel.",
    "If the timer is not reset, it will not continue firing periodically.",
])
story.append(PageBreak())

p("Quest 10: Pixel Donut", "Section")
p("The big idea", "Sub")
p("Quest 10 combines the framebuffer from Quest 8 with the interrupts from Quest 9. The timer decides when to draw the next frame.", "Quote")
p("Key functions", "Sub")
p("<b>donut_simple()</b>: prepares the large canvas and starts the first system-timer alarm.", "Body")
p("<b>sys_timer_irq_simple()</b>: confirms and clears the timer interrupt, draws a frame, and schedules the next alarm.", "Body")
p("<b>draw_frame()</b>: calculates the donut shape, depth, brightness, color, and pixel locations for one frame.", "Body")
p("Flow", "Sub")
p("kernel_main() &rarr; donut_simple() &rarr; start timer &rarr; wfi waits &rarr; timer expires &rarr; handle_irq() &rarr; sys_timer_irq_simple() &rarr; draw_frame() &rarr; schedule next timer &rarr; repeat", "Flow")
p("Why use wfi?", "Sub")
p("wfi means wait for interrupt. The CPU sleeps instead of constantly checking the timer in a busy loop, which saves CPU time.", "Body")
p("What if?", "Sub")
bullets([
    "If donut_simple() is not called, the canvas and timer are not prepared.",
    "If handle_irq() does not call sys_timer_irq_simple(), the timer fires but no frame is drawn.",
    "If the timer status is not cleared, the interrupt may happen again immediately.",
    "If the next timer value is not set, only one frame is drawn.",
    "If depth testing is removed, faraway donut surfaces can cover nearby surfaces.",
])

story.append(PageBreak())
p("What You See in QEMU", "Section")
p("Quest 8: colored screen sections", "Sub")
p("The program creates a large virtual framebuffer divided into four colored sections. The QEMU display shows one section at a time as the offset changes. This demonstrates moving the viewing window without redrawing the whole screen.", "Body")
p("Quest 9: timer work in the background", "Sub")
p("There is usually no special picture for Quest 9. The timer acts like an alarm: it expires, sends an IRQ, and causes the CPU to run the interrupt handler. This hidden process is what makes timed animation possible.", "Body")
p("Quest 10: the rotating donut", "Sub")
p("The QEMU window shows the result of Quest 10. Every timer interrupt calls <b>draw_frame()</b>. That function draws one donut picture with a slightly different rotation. Many pictures shown one after another look like motion.", "Body")
p("Live demo flow", "Sub")
p("Build the kernel &rarr; start QEMU &rarr; framebuffer initializes &rarr; donut_simple() starts the timer &rarr; wfi waits &rarr; timer IRQ calls handle_irq() &rarr; sys_timer_irq_simple() calls draw_frame() &rarr; the next timer is scheduled", "Flow")
p("What to say while it runs", "Sub")
p("Quest 8 prepares the screen by creating a larger framebuffer and selecting which part is visible. Quest 9 makes the timer interrupt the CPU. Quest 10 connects them: every timer interrupt draws a new rotated donut frame. The CPU waits between frames with wfi instead of wasting time in a busy loop.", "Quote")
p("Run command", "Sub")
p("cd \"/mnt/d/UTA/CSE 3320 - OS/lab1-1/lab1\"<br/>export PLAT=rpi3qemu<br/>./makeall.sh<br/>./run-rpi3qemu.sh full", "Flow")
p("Expected terminal line", "Sub")
p("Using QEMU: /home/alvin/qemu-9.1.1/build/qemu-system-aarch64", "Flow")

story.append(PageBreak())
p("30-second presentation", "Section")
p("Quest 8 demonstrates framebuffer offsets. The program creates a virtual framebuffer containing four colored sections, then changes the offset to choose which section is visible. This is efficient because it changes the viewport instead of redrawing the screen.", "Body")
p("Quest 9 enables timer interrupts. When the timer expires, the CPU uses the exception vector table to find the IRQ handler. The handler saves the registers, calls handle_irq(), handles the timer, restores the registers, and returns. The timer is reset so it can fire again.", "Body")
p("Quest 10 uses that interrupt system to animate the donut. donut_simple() initializes the framebuffer and starts the timer. Each timer interrupt calls sys_timer_irq_simple(), which clears the interrupt, calls draw_frame(), and schedules the next frame. Repeating this creates the animation.", "Body")
gap(12)
p("One sentence to remember", "Sub")
p("Quest 8 prepares the screen, Quest 9 delivers the alarm, and Quest 10 draws a new picture whenever the alarm rings.", "Quote")

doc.build(story, onFirstPage=footer, onLaterPages=footer)
print(output)
