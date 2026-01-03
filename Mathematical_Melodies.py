import streamlit as st, music21 as m21
import Music_Generation as mg
import Music_Analysis as ma

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
instrument_choice = st.multiselect("Which instruments do you want? ", list(mg.instruments_dict.keys()))
instrument = mg.instruments_dict[instrument_choice[0]] if instrument_choice else 0
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
        mg.generate_midi("mathematical_melody.mid", instrument_choice, key, numMeasures, time_signature)
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
        st.header("Individual Instrument Analysis")

        part_analyses = ma.individual_analysis("mathematical_melody.mid")
        individual_interpretation = ma.individual_analysis_output(part_analyses)

        for part_name, interpretations in individual_interpretation.items():
            st.subheader(f"Instrument: {part_name}")

            st.write("**Interval Distribution:**")
            st.write(interpretations['step_size'])

            st.write("**Rhythm Density:**")
            st.write(interpretations['rhythm'])

            st.write("**Harmonic Complexity:**")
            st.write(interpretations['harmony'])

            st.write("**Melodic Contour:**")
            st.write(interpretations['melodic_contour'])

    