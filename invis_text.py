# import tkinter

# def on_entry_click_input(event, entry_widget):
#     if entry_widget.get() == default_text:
#         entry_widget.delete(0, "end")
#         entry_widget.config(fg='black')

# def on_focus_out_input(event, entry_widget, default_text):
#     if entry_widget.get() == "":
#         entry_widget.insert(0, default_text)
#         entry_widget.config(fg='grey')

# def inv_text_input(default_text, input_text):
#     input_text.insert(0, default_text)
#     input_text.bind("<FocusIn>", lambda event: on_entry_click_input(event, input_text))
#     input_text.bind("<FocusOut>", lambda event: on_focus_out_input(event, input_text, default_text))
    
    
    
    
# def on_entry_click_output(event, entry_widget):
#     if entry_widget.get("1.0", "end-1c") == default_text:
#         entry_widget.delete("1.0", "end")
#         entry_widget.config(fg='black')

# def on_focus_out_output(event, entry_widget, default_text):
#     if entry_widget.get("1.0", "end-1c") == "":
#         entry_widget.insert("1.0", default_text)
#         entry_widget.config(fg='grey')
        
# def inv_text_output(default_text, output_text):
#     #output_text.pack()
#     output_text.insert("1.0", default_text)
#     output_text.bind("<FocusIn>", lambda event: on_entry_click_output(event, output_text))
#     output_text.bind("<FocusOut>", lambda event: on_focus_out_output(event, output_text, default_text))