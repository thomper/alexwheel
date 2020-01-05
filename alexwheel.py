#! /usr/bin/python3

from collections import namedtuple
import plotly.express as px
import sys


Emotion = namedtuple('Emotion', ('noun', 'adjective', 'parent'))

ROOTS = (Emotion('Joy',      'Joyful', ''),
         Emotion('Surprise', 'Surprised', ''),
         Emotion('Sadness',  'Sad', ''),
         Emotion('Anger',    'Angry', ''),
         Emotion('Fear',     'Fearful', ''),
         Emotion('Love',     'Loveful', ''))  # TODO: not sure about 'loveful'

MIDDLE = (Emotion('Enthrallment', 'Enthralled', 'Joy'),
          Emotion('Elation', 'Elated', 'Joy'),
          Emotion('Enthusiasm', 'Enthusiastic', 'Joy'),
          Emotion('Optimism', 'Optimistic', 'Joy'),
          Emotion('Pride', 'Proud', 'Joy'),
          Emotion('Cheerfulness', 'Cheerful', 'Joy'),
          Emotion('Happiness', 'Happy', 'Joy'),
          Emotion('Contentment', 'Content', 'Joy'),
          Emotion('???Moved???', 'Moved', 'Surprise'),  # TODO
          Emotion('???Overcome???', 'Overcome', 'Surprise'),  # TODO
          Emotion('Amazement', 'Amazed', 'Surprise'),
          Emotion('Confusion', 'Confused', 'Surprise'),
          Emotion('Stun', 'Stunned', 'Surprise'),
          Emotion('Despair', 'Despairing', 'Sadness'),
          Emotion('Neglect', 'Neglected', 'Sadness'),
          Emotion('Shame', 'Shameful', 'Sadness'),
          Emotion('Disappointment', 'Disappointed', 'Sadness'),
          Emotion('Depression', 'Depressed', 'Sadness'),
          Emotion('Sorrow', 'Sorrowful', 'Sadness'),
          Emotion('Suffering', 'Suffering', 'Sadness'),
          Emotion('Disgust', 'Disgusted', 'Anger'),
          Emotion('Envy', 'Envious', 'Anger'),
          Emotion('Irritability', 'Irritable', 'Anger'),
          Emotion('Exasparation', 'Exasparated', 'Anger'),
          Emotion('Rage', 'Enraged', 'Anger'),
          Emotion('Horror', 'Horrified', 'Fear'),
          Emotion('Nervousness', 'Nervous', 'Fear'),
          Emotion('Insecurity', 'Insecure', 'Fear'),
          Emotion('Terror', 'Terrified', 'Fear'),
          Emotion('Scaredness', 'Scared', 'Fear'),
          Emotion('Peace', 'Peaceful', 'Love'),
          Emotion('Tenderness', 'Tender', 'Love'),
          Emotion('Desire', 'Desirous', 'Love'),
          Emotion('Longingness', 'Longing', 'Love'),
          Emotion('Affection', 'Affectionate', 'Love'))

LEAVES = (Emotion('Rapture', 'Rapt', 'Enthrallment'),
          Emotion('Enchantment', 'Enchanted', 'Enthrallment'),
          Emotion('Jubilation', 'Jubilant', 'Elation'),
          Emotion('Euphoria', 'Euphoric', 'Elation'),
          Emotion('Zeal', 'Zealous', 'Enthusiasm'),
          Emotion('Excitement', 'Excited', 'Enthusiasm'),
          Emotion('Hope', 'Hopeful', 'Optimism'),
          Emotion('Eagerness', 'Eager', 'Optimism'),
          Emotion('Illustriousness', 'Illustrious', 'Pride'),
          Emotion('Triumph', 'Triumphant', 'Pride'),
          Emotion('Bliss', 'Blissful', 'Cheerfulness'),
          Emotion('Joviality', 'Jovial', 'Cheerfulness'),
          Emotion('Delight', 'Delighted', 'Happiness'),
          Emotion('Amusement', 'Amused', 'Happiness'),
          Emotion('Satisfaction', 'Satisfied', 'Contentment'),
          Emotion('Pleasure', 'Pleased', 'Contentment'),
          Emotion('???Touched???', 'Touched', '???Moved???'),  # TODO
          Emotion('Stimulation', 'Stimulated', '???Moved???'),
          Emotion('Astoundment', 'Astounded', '???Overcome???'),
          Emotion('Speechlessness', 'Speechless', '???Overcome???'),
          Emotion('Awe', 'Awestruck', 'Amazement'),
          Emotion('Astonishment', 'Astonished', 'Amazement'),
          Emotion('Perplexity', 'Perplexed', 'Confusion'),
          Emotion('Disillusionment', 'Disillusioned', 'Confusion'),
          Emotion('Dismay', 'Dismayed', 'Stun'),
          Emotion('Shock', 'Shocked', 'Stun'),
          Emotion('Powerlessness', 'Powerless', 'Despair'),
          Emotion('Grief', 'Grieving', 'Despair'),
          Emotion('Loneliness', 'Lonely', 'Neglect'),
          Emotion('Isolation', 'Isolated', 'Neglect'),
          Emotion('Guilt', 'Guilty', 'Shame'),
          Emotion('Regret', 'Regretful', 'Shame'),
          Emotion('Displeasure', 'Displeased', 'Disappointment'),
          Emotion('Dismay', 'Dismayed', 'Disappointment'),
          Emotion('Hurt', 'Hurt', 'Suffering'),
          Emotion('Agony', 'Agonised', 'Suffering'),
          Emotion('Revulsion', 'Revolted', 'Disgust'),
          Emotion('Contempt', 'Contemptuous', 'Disgust'),
          Emotion('Jealousy', 'Jealous', 'Envy'),
          Emotion('Resentment', 'Resentful', 'Envy'),
          Emotion('Aggravation', 'Aggravated', 'Irritability'),
          Emotion('Annoyance', 'Annoyed', 'Irritability'),
          Emotion('Frustration', 'Frustrated', 'Exasparation'),
          Emotion('Agitation', 'Agitated', 'Exasparation'),
          Emotion('Hostility', 'Hostile', 'Rage'),
          Emotion('Hate', 'Hateful', 'Rage'),
          Emotion('Dread', 'Dreading', 'Horror'),
          Emotion('Mortification', 'Mortified', 'Horror'),
          Emotion('Anxiety', 'Anxious', 'Nervousness'),
          Emotion('Worry', 'Worried', 'Nervousness'),
          Emotion('Inadequacy', 'Inadequate', 'Insecurity'),
          Emotion('Inferiority', 'Inferior', 'Insecurity'),
          Emotion('Hysteria', 'Hysterical', 'Terror'),
          Emotion('Panic', 'Panicked', 'Terror'),
          Emotion('Helplessness', 'Helpless', 'Scaredness'),
          Emotion('Fright', 'Frightened', 'Scaredness'),
          Emotion('Relief', 'Relieved', 'Peace'),
          Emotion('Compassion', 'Compassionate', 'Tenderness'),
          Emotion('Caringness', 'Caring', 'Tenderness'),
          Emotion('Infatuation', 'Infatuated', 'Desire'),
          Emotion('Passion', 'Passionate', 'Desire'),
          Emotion('Attraction', 'Attracted', 'Longingness'),
          Emotion('Sentimentality', 'Sentimental', 'Longingness'),
          Emotion('Fondness', 'Fond', 'Affection'),
          Emotion('Romance', 'Romantic', 'Affection'))

EMOTIONS = ROOTS + MIDDLE + LEAVES


def adjective_form(noun):
    if not noun:
        return noun
    emotion = next(iter({e if e.noun == noun else None for e in EMOTIONS} - {None}))
    return emotion.adjective


def build_dict(use_nouns=True):
    return {'names': [e.noun if use_nouns else e.adjective for e in EMOTIONS],
            'parents': [e.parent if use_nouns else adjective_form(e.parent) for e in EMOTIONS],
            'values': [1] * len(EMOTIONS)}

def get_args():
    if len(sys.argv) == 2:
        return {'use_nouns': sys.argv[1] not in ('-a', '--adjectives')}
    return {'use_nouns': True}


def main():
    use_nouns = get_args()['use_nouns']
    fig = px.sunburst(build_dict(use_nouns), names='names', parents='parents', values='values')
    fig.show()


if __name__ == '__main__':
    main()
