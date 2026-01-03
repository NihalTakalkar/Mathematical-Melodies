import streamlit as st, music21 as m21


def analyze_music(file_path):

    # Load the MIDI file
    score = m21.converter.parse(file_path)

    all_notes = score.flat.notes
    pitched_notes = [note for note in all_notes if isinstance(note, m21.note.Note)]

    # Analyze interval distribution
    def analyze_intervals(notes):
        intervals = []   
        
        for i in range(1, len(notes)):
            interval = abs(notes[i].pitch.midi - notes[i-1].pitch.midi)
            intervals.append(interval)
        interval_distribution = {}
        for interval in intervals:
            if interval in interval_distribution:
                interval_distribution[interval] += 1
            else:
                interval_distribution[interval] = 1
        return interval_distribution
    interval_distribution = analyze_intervals(pitched_notes)
    
    def step_size_distribution(step_size, mean_interval):
        return mean_interval / step_size if step_size != 0 else 0
    
    mean_interval = sum(interval * count for interval, count in interval_distribution.items()) / sum(interval_distribution.values()) if sum(interval_distribution.values()) != 0 else 0
    step_size_dist = step_size_distribution(1, mean_interval)
    
    def rhythm_density(midi_path):
        score = m21.converter.parse(midi_path)
        total_duration = score.highestTime
        note_count = len(score.flat.notes)
        return note_count / total_duration if total_duration != 0 else 0
    rhythm_density_value = rhythm_density(file_path)
    
    def harmonic_complexity(midi_path):
        score = m21.converter.parse(midi_path)
        chords = score.chordify().recurse().getElementsByClass('Chord')
        unique_chords = set()
        
        for chord in chords:
            unique_chords.add(tuple(sorted(p.pitchClass for p in chord.pitches)))
        
        return len(unique_chords) / len(chords) if len(chords) != 0 else 0
    harmonic_complexity_value = harmonic_complexity(file_path)
    
    def melodic_contour(notes):
        contour = []
        
        for i in range(1, len(notes)):
            if notes[i].pitch.midi > notes[i-1].pitch.midi:
                contour.append('up')
            elif notes[i].pitch.midi < notes[i-1].pitch.midi:
                contour.append('down')
            else:
                contour.append('same')
        
        return contour
    melodic_contour_value = melodic_contour(pitched_notes)

    return {
        'step_size_distribution': step_size_dist,
        'rhythm_density': rhythm_density_value,
        'harmonic_complexity': harmonic_complexity_value,
        'melodic_contour': melodic_contour_value
    }

def analysis_output(results):

        interpretation = {}

        step = results['step_size_distribution']
        if step < 5:
            interpretation['step_size'] = "The melody has small step sizes, giving a smooth melodic movement."
        elif step < 10:
            interpretation['step_size'] = "The melody has moderate step sizes, giving a balanced melodic contour."
        else:
            interpretation['step_size'] = "The melody has large step sizes, creating a more dramatic melodic effect."

        rhythm = results['rhythm_density']
        if rhythm < 2:
            interpretation['rhythm'] = "The melody has low rhythm density, resulting in a sparse rhythmic texture."
        elif rhythm < 4:
            interpretation['rhythm'] = "The melody has moderate rhythm density, providing a balanced rhythmic feel."
        else:
            interpretation['rhythm'] = "The melody has high rhythm density, creating a lively and energetic rhythmic texture."

        harmony = results['harmonic_complexity']
        if harmony < 0.3:
            interpretation['harmony'] = "The melody has simple harmonic structures, making it easy to follow."
        elif harmony < 0.6:
            interpretation['harmony'] = "The melody has moderately complex harmonic structures, adding interest."
        else:
            interpretation['harmony'] = "The melody has complex harmonic structures, providing rich musical depth."

        contour = results['melodic_contour']
        up_moves = contour.count('up')
        down_moves = contour.count('down')
        if up_moves > down_moves:
            interpretation['melodic_contour'] = "The melody generally ascends, creating a sense of uplift."
        elif down_moves > up_moves:
            interpretation['melodic_contour'] = "The melody generally descends, evoking a calming effect."
        else:
            interpretation['melodic_contour'] = "The melody has a balanced contour, providing variety."


        return interpretation