import streamlit as st, music21 as m21
import Music_Generation as mg

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

if st.button("Generate Musical MIDI Files"):
    if instrument_choice and Key != "None Selected" and numMeasures > 0 and time_signature != "None Selected":
        mg.generate_midi("mathematical_melody.mid", instrument_choice, key, numMeasures, time_signature)
        st.success("Your MIDI file has been generated!")

        with open("mathematical_melody.mid", "rb") as file:
            st.button("Play MIDI file", on_click=lambda: m21.converter.parse("mathematical_melody.mid").show('midi'))


    else:
        st.error("Please fill in all required fields.")
