function addSections( editor, sections ){
    for(j=0; sections.length; j++){
        section = sections[j]
        
        sect = new THREE.Object3D();
        sect.name = 'Section ' + String(j+1)
        sect.userData = {'id': j+1,
                        'section_id': section.section_id,
                        'material': section.material,
                        'dimensions': section.dimensions,
                        'type': section.type,
                        'A': section.A,
                        'Ix': section.Ix,
                        'Iy': section.Iy,
                        'Iz': section.Iz};

        editor.sections.add( sect );
        
        
    };
    
};