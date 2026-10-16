"""Day 1: build the matching rules. The initial skeleton returns no results."""
from language_policy import language_matches


def shared_interests(wanted, programme):
    matches = []
    for interest in wanted:
        # TODO 1: If this interest is in programme["interest_tags"],
        # add it to matches. Avoid adding the same interest twice.
        # ถ้าความสนใจตรงกับแท็ก ให้เพิ่มใน matches โดยไม่เพิ่มซ้ำ
        pass
    return matches


def find_programmes(programmes, region, interest_tags, format, include_unresolved, match_all=True):
    results = []
    for programme in programmes:
        if not match_all:
            if region =="any" or format=='any':
                results.append(programme)
                continue
            if programme['region']==region:
                results.append(programme)
                continue
            
            if programme['teaching_language'] == format:
                results.append(programme)
                continue
            elif programme['teaching_language'] == 'unknown' and include_unresolved:
                results.append(programme)
                continue
            for tag in interest_tags:
                if tag in programme['interest_tags']:
                    results.append(programme)
                    break
        else:
            if region!="any" and programme['region']!=region:
                continue
            print(programme['teaching_language'])
            if not include_unresolved:
                if format!="any" and programme['teaching_language']!=format:
                    continue
            else:
                if format!="any" and programme['teaching_language']!=format and programme['teaching_language']!='unknown':
                    continue
            
            if interest_tags!=[]:
                
                for tag in interest_tags:
                    if tag in programme['interest_tags']:
                        results.append(programme)
                        break
            else:
                
                results.append(programme)
    # Stretch: sort by the number of shared interests, largest first.
    # ต่อยอด: เรียงตามจำนวนความสนใจที่ตรง มากก่อน
    return results

from data_loader import load_programmes
print(load_programmes())
print(len(find_programmes(programmes=load_programmes(),
                      region="north",
                      format="th",
                      interest_tags=[],
                      include_unresolved=True,
                      match_all=True)))