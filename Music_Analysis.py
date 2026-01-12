import streamlit as st, music21 as m21
from Music_Generation import string_instruments, woodwind_instruments, brass_instruments, percussion_instruments, pianos

def overall_analysis(file_path):
    score = m21.converter.parse(file_path)
    notes = score.flat.notes
    pitched_notes = [note for note in notes if isinstance(note, m21.note.Note)]

    analysis_results = analysis(score)

    return analysis_results

def analysis(stream):

    all_notes = stream.flat.notes
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
    
    def rhythm_density(stream):
        total_duration = stream.highestTime
        num_notes = len(pitched_notes)
        return num_notes / total_duration if total_duration != 0 else 0
    rhythm_density_value = rhythm_density(stream)
        
    
    def harmonic_complexity(stream):
        score = stream if isinstance(stream, m21.stream.Stream) else m21.converter.parse(stream)
        chords = score.chordify().recurse().getElementsByClass(m21.chord.Chord)

        unique_chords = set()
        for chord in chords:
            pcs = tuple(sorted(p.pitchClass for p in chord.pitches))
            unique_chords.add(pcs)

        return len(unique_chords) / len(chords) if chords else 0
    harmonic_complexity_value = harmonic_complexity(stream)
    
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

def overall_analysis_output(results):

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

def individual_analysis(file_path):

    score = m21.converter.parse(file_path)
    part_analyses = {}

    for part in score.parts:
        part_name = part.partName if part.partName else "Unknown Instrument"
        notes = part.flat.notes
        pitched_notes = [note for note in notes if isinstance(note, m21.note.Note)]

        analysis_results = analysis(part)

        part_analyses[part_name] = analysis_results

    return part_analyses

def concept_works(instrument, concept):

     # STRINGS
    if instrument in string_instruments:
        if concept == "Fibonacci Sequence":
            return True, (
                "The Fibonacci Sequence creates gradual pitch expansion, "
                "which aligns well with the smooth, lyrical phrasing of string instruments."
            )
        if concept == "Prime Numbers":
            return True, (
                "Prime Numbers introduce irregular but expressive interval patterns, "
                "which string instruments can articulate clearly."
            )
        if concept == "Multiples of 2":
            return True, (
                "Multiples of 2 produce predictable interval spacing, "
                "supporting stable melodic motion on string instruments."
            )
        if concept == "Multiples of 5":
            return False, (
                "Multiples of 5 create large, abrupt jumps that reduce melodic continuity, "
                "which is less suitable for sustained string phrasing."
            )

    # WOODWINDS
    if instrument in woodwind_instruments:
        if concept in {"Fibonacci Sequence", "Prime Numbers"}:
            return True, (
                "This concept creates varied but singable melodic contours, "
                "which woodwind instruments handle well due to their agility."
            )
        if concept == "Multiples of 2":
            return True, (
                "Even-number spacing results in balanced melodic movement, "
                "which suits the controlled breath phrasing of woodwinds."
            )
        if concept == "Multiples of 5":
            return False, (
                "Multiples of 5 tend to produce wide intervallic jumps that can disrupt "
                "woodwind phrasing and intonation stability."
            )

    # BRASS
    if instrument in brass_instruments:
        if concept == "Fibonacci Sequence":
            return True, (
                "The gradual expansion of Fibonacci intervals complements the natural overtone "
                "series of brass instruments."
            )
        if concept == "Prime Numbers":
            return True, (
                "Prime-based spacing creates bold, declarative melodic shapes that align "
                "with the strong projection of brass instruments."
            )
        return False, (
            "Highly repetitive or rhythm-driven sequences limit the expressive range "
            "of brass instruments."
        )

    # PERCUSSION
    if instrument in percussion_instruments:
        if concept == "Multiples of 2":
            return True, (
                "Multiples of 2 reinforce steady rhythmic subdivision, "
                "which is fundamental to percussion performance."
            )
        if concept == "Multiples of 5":
            return True, (
                "Multiples of 5 introduce polyrhythmic groupings that enhance "
                "percussive complexity."
            )
        return False, (
            "Pitch-driven mathematical sequences are less effective for "
            "unpitched percussion instruments."
        )

    # KEYBOARD
    if instrument in pianos:
        return True, (
            "Keyboard instruments support both harmonic and rhythmic structures, "
            "making them compatible with all mathematical concepts."
        )

    # CHOIR
    if instrument == "Choir":
        if concept in {"Fibonacci Sequence", "Prime Numbers"}:
            return True, (
                "These sequences produce expressive melodic contours suitable "
                "for vocal phrasing."
            )
        return False, (
            "Highly repetitive numeric patterns can sound mechanical when applied to voices."
        )

    return False, "This concept is not recommended for the selected instrument."

def individual_analysis_output(part_analyses):

    interpretations = {}

    for part_name, results in part_analyses.items():
        interpretation = {}

        
        step = results['step_size_distribution']
        interpretation['step_size'] = (
            f"The {part_name} has small step sizes, giving smooth melodic movement."
            if step < 5 else
            f"The {part_name} has moderate step sizes, giving balanced melodic motion."
            if step < 10 else
            f"The {part_name} has large step sizes, creating dramatic melodic leaps."
        )

        rhythm = results['rhythm_density']
        interpretation['rhythm'] = (
            f"The {part_name} has low rhythmic density."
            if rhythm < 2 else
            f"The {part_name} has moderate rhythmic activity."
            if rhythm < 4 else
            f"The {part_name} has high rhythmic activity."
        )

        harmony = results['harmonic_complexity']
        interpretation['harmony'] = (
            f"The {part_name} has simple harmonic structures."
            if harmony < 0.3 else
            f"The {part_name} has moderately complex harmony."
            if harmony < 0.6 else
            f"The {part_name} has rich harmonic complexity."
        )

        contour = results['melodic_contour']
        interpretation['melodic_contour'] = (
            f"The {part_name} generally ascends."
            if contour.count('up') > contour.count('down') else
            f"The {part_name} generally descends."
            if contour.count('down') > contour.count('up') else
            f"The {part_name} has a balanced melodic contour."
        )

        interpretations[part_name] = interpretation

    return interpretations
