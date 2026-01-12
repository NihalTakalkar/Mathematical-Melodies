import streamlit as st, music21 as m21
import Music_Generation as mg
import Music_Analysis as ma
import pandas as pd

st.set_page_config(layout="wide")

if st.button("🔄 Make a new song"):
    st.session_state.midi_generated = False
    st.session_state.analysis_done = False
    st.session_state.overall_analysis = None
    st.session_state.individual_analysis_done = False
    st.session_state.instrument_choice = []
    st.session_state.selected_key = "None Selected"
    st.session_state.major_or_minor = "Major"
    st.session_state.numMeasures = 4
    st.session_state.time_signature = "None Selected"

# Default session state variables
if "midi_generated" not in st.session_state:
    st.session_state.midi_generated = False

if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False

if "overall_analysis_done" not in st.session_state:
    st.session_state.overall_analysis_done = None

if "individual_analysis" not in st.session_state:
    st.session_state.individual_analysis_done = False

if "instrument_choice" not in st.session_state:
    st.session_state.instrument_choice = []

if "selected_key" not in st.session_state:
    st.session_state.selected_key = "None Selected"

if "major_or_minor" not in st.session_state:
    st.session_state.major_or_minor = "Major"

if "numMeasures" not in st.session_state:
    st.session_state.numMeasures = 4

if "time_signature" not in st.session_state:
    st.session_state.time_signature = "None Selected"

# Streamlit App Interface

st.title("Mathematical Melodies")

# Initialize session dictionary if it doesn't exist
if "inst_math_choices" not in st.session_state:
    st.session_state.inst_math_choices = {}

instrument_choice = st.multiselect(
    "Which instruments do you want?",
    list(mg.instruments_dict.keys())
)

for instrument in instrument_choice:
    math_choice = st.selectbox(
        f"Select mathematical concept for {instrument}:",
        ["Fibonacci Sequence", "Prime Numbers", "Multiples of 2", "Multiples of 5"],
        key=f"math_select_{instrument}"
    )

    # Update only this instrument's concept
    st.session_state.inst_math_choices[instrument] = math_choice

    st.write(f"You selected {math_choice} for the {instrument}.")

Key = st.selectbox("Select a key: ", 
                   ("None Selected", "C", "C♯/D♭", "D", "D♯/E♭", "E", "F", "F♯/G♭", "G", 
                    "G♯/A♭", "A", "A♯/B♭", "B"))

if Key != "None Selected":

    major_or_minor = st.selectbox("Major or Minor? ", ("Major", "Minor"))

    key = mg.key_to_midi(Key, major_or_minor)
       
    

numMeasures = st.number_input("How many measures?", min_value=1, max_value=32, value=4)
time_signature = st.selectbox("What time signature?", ("None Selected", "4/4", "3/4", "6/8"))

# Generate MIDI File
if st.button("Generate Musical MIDI"):
    if instrument_choice and Key != "None Selected" and numMeasures > 0 and time_signature != "None Selected":
        mg.generate_midi("mathematical_melody.mid", st.session_state.inst_math_choices, key, numMeasures, time_signature)
        st.session_state.midi_generated = True
        st.success("Your MIDI file has been generated!")

        

    else:
        st.error("Please fill in all required fields.")

# Music Analysis
if st.session_state.midi_generated:


    col1, col2 = st.columns(2)
    with col1:
        play_music = st.button("▶ Play Generated Music", key="play_btn")

    with col2:
        analyze_music_btn = st.button("🔍 Analyze Generated Music", key="analyze_btn")

    if play_music:
        m21.converter.parse("mathematical_melody.mid").show("midi")

    if analyze_music_btn:
        st.session_state.overall_analysis = ma.overall_analysis("mathematical_melody.mid")
        st.session_state.analysis_done = True


    if st.session_state.analysis_done:
        st.header("Music Analysis")

        interpretation = ma.overall_analysis_output(st.session_state.overall_analysis)

        st.subheader("Interval Distribution")
        st.write(interpretation['step_size'])

        st.subheader("Rhythm Density")
        st.write(interpretation['rhythm'])

        st.subheader("Harmonic Complexity")
        st.write(interpretation['harmony'])

        st.subheader("Melodic Contour")
        st.write(interpretation['melodic_contour'])

        st.space("medium")

        if st.button("Analyze Individual Instrument Parts"):
            st.session_state.individual_analysis_done = True

    
    if st.session_state.individual_analysis_done:
        st.header("Instrument Analysis Results")

        # Run analysis once
        part_analyses = ma.individual_analysis("mathematical_melody.mid")
        individual_interpretation = ma.individual_analysis_output(part_analyses)

        # Build data for table
        instruments = []
        math_concepts = []
        interval_distribution = []
        rhythm_density = []
        harmonic_complexity = []
        melodic_contour = []
        works_well = []

        for instr in st.session_state.inst_math_choices.keys():
            instruments.append(instr)
            math_concepts.append(st.session_state.inst_math_choices.get(instr, "N/A"))

            # If this instrument was analyzed, get its metrics; otherwise, use "N/A"
            metrics = individual_interpretation.get(instr, {})
            interval_distribution.append(metrics.get('step_size', "N/A"))
            rhythm_density.append(metrics.get('rhythm', "N/A"))
            harmonic_complexity.append(metrics.get('harmony', "N/A"))
            melodic_contour.append(metrics.get('melodic_contour', "N/A"))
            works, explanation = ma.concept_works(instr, st.session_state.inst_math_choices.get(instr, "N/A"))
            works_well.append("Yes - " + explanation if works else "No - " + explanation)

        # Create DataFrame
        summary_df = pd.DataFrame({
            "Instrument": instruments,
            "Math Concept Used": math_concepts,
            "Interval Distribution": interval_distribution,
            "Rhythm Density": rhythm_density,
            "Harmonic Complexity": harmonic_complexity,
            "Melodic Contour": melodic_contour,
            "Does the concept work well for this instrument?": works_well
        })

        # Display table
        rows = len(summary_df)
        row_height = 45
        header_height = 60
        padding_fix = 90

        table_height = max(
            200,
            header_height + row_height * rows - padding_fix
        )

        st.dataframe(
            summary_df,
            use_container_width=True,
            height=table_height
        )

    