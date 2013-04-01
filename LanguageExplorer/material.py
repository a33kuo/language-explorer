from flask import Module
from flask import redirect,request,session
from flask import render_template

from LanguageExplorer.model import Context,CONTEXT_TYPE,Dialogue,SuppMaterial
from LanguageExplorer.model import Assertion,Concept,Relation

material = Module(__name__)

@material.route('/context/')
@material.route('/context/<context_id>')
def context(context_id=None):
    list_mode = True
    if context_id == None:
        # Does not pass any argument - show context list.
        location_contexts = Context.get_context_list(session['user_language'], \
                                                     CONTEXT_TYPE.location)
        event_contexts = Context.get_context_list(session['user_language'], \
                                                  CONTEXT_TYPE.event)
        return render_template('context.html', list_mode=list_mode, \
                               locations=location_contexts, events=event_contexts)
    else:
        # Pass context id - show concept, dialogues, and supplementary materials.
        list_mode = False
        context = Context.get_context(context_id)
        concepts = context.concepts.all()
        dialogues = context.dialogues.all()
        supp_materials = context.materials.all()
        return render_template('context.html', list_mode=list_mode, \
                               context=context, concepts=concepts, \
                               dialogues=dialogues, supp_materials=supp_materials)

# TODO(a33kuo): Use ajax to send new context text.
@material.route('/add_context/', methods=['GET', 'POST'])
def new_context():
    if request.method == 'POST':
        text = request.form['context_name']
        if text.strip() == "":
            return render_template('add_context.html', \
                                   error="Context name cannot be blank.")
        ctype = request.form['context_type']
        context = Context(text, session['user_language'], \
                          ctype=ctype)
        context.add()
        return redirect('/context/')
    else:
        return render_template('add_context.html')

@material.route('/concept/<context_id>/<concept_id>', methods=['POST', 'GET'])
def concept(context_id=None, concept_id=None):
    if concept_id is not None:
        concept = Concept.get_concept_by_id(concept_id)
    else:
        return render_template('concept.html', error="Invalid concept.")
    if context_id is not None:
        context = Context.get_context(context_id)
    else:
        return render_template('concept.html', error="Invalid context.")
    assertions = concept.get_assertions()
    cocnept_assertions = context.assertions.all()
    return render_template('concept.html')

@material.route('/add_concept/<context_id>', methods=['POST', 'GET'])
def new_concept(context_id=None):
    if request.method == 'POST':
        text = request.form['concept_name']
        if text.strip() == "":
            return render_template('add_concept.html', \
                                   context_id=context_id, \
                                   error="Concept cannot be blank.")
        # TODO(a33kuo): Should be replaced by get_or_create() method.
        concept = Concept.get_concept(text, session['user_language'])
        if concept is None:
            concept = Concept(text, session['user_language'])
            concept.add()
        context = Context.get_context(context_id)
        concept.add_context(context)
        if context_id is not None:
            return redirect('/context/' + context_id)
        else:
            return redirect('/context/')
    else:
        return render_template('add_concept.html', context_id=context_id)

def new_assertion():
    pass

def dialogue():
    pass

@material.route('/add_dialogue/<context_id>', methods=['GET', 'POST'])
def new_dialogue(context_id=None):
    if request.method == 'POST':
        text = request.form['dialogue_text']
        if text.strip() == "":
            return render_template('add_dialogue.html', \
                                   context_id=context_id, \
                                   error="Dialogue cannot be blank.")
        dialogue = Dialogue(text, session['user_language'])
        dialogue.add()
        context = Context.get_context(context_id)
        dialogue.add_context(context)
        if context_id is not None:
            return redirect('/context/' + context_id)
        else:
            return redirect('/context/')
    else:
        return render_template('add_dialogue.html', context_id=context_id)

@material.route('/add_supp_material/<context_id>', methods=['GET', 'POST'])
def new_supp_material(context_id=None):
    if request.method == 'POST':
        text = request.form['material_text']
        if text.strip() == "":
            return render_template('add_supp_material.html', \
                                   context_id=context_id, \
                                   error="Supplementary material cannot be blank.")
        supp = SuppMaterial(text, session['user_language'])
        supp.add()
        context = Context.get_context(context_id)
        supp.add_context(context)
        if context_id is not None:
            return redirect('/context/' + context_id)
        else:
            return redirect('/context/')
    else:
        return render_template('add_supp_material.html', context_id=context_id)

