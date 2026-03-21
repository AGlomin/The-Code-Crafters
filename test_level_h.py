from LevelHandler import loadLevel

def test_load_level_basic(tmp_path):
   
    test_file = tmp_path / "test_level.txt" #create temp test file
    
    test_file.write_text(
        "5,5,1,1,2,2,3,3,0,0,4,4\n"
        "E1,1,1,E2,2,2\n"
        "E3,3,3\n"
    )
    result = loadLevel(test_file)
    assert result[0]==5  
    assert result[1]==5  
    assert result[2]==1  
    assert result[8]==[[0,0],[4,4]]  
    assert len(result[9])==2 