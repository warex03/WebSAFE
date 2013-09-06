import sys
    
def impactLayerAttribution(theKeywords, theInaSAFEFlag=False):
    """Make a little table for attribution of data sources used in impact.

    Args:
        * theKeywords: dict{} - a keywords dict for an impact layer.
        * theInaSAFEFlag: bool - whether to show a little InaSAFE promotional
            text in the attribution output. Defaults to False.

    Returns:
        str: an html snippet containing attribution information for the impact
            layer. If no keywords are present or no appropriate keywords are
            present, None is returned.

    Raises:
        None
    """
    if theKeywords is None:
        return None
    myReport = ''
    myJoinWords = ' - %s ' % tr('sourced from')
    myHazardDetails = tr('Hazard details')
    myHazardTitleKeyword = 'hazard_title'
    myHazardSourceKeyword = 'hazard_source'
    myExposureDetails = tr('Exposure details')
    myExposureTitleKeyword = 'exposure_title'
    myExposureSourceKeyword = 'exposure_source'

    if myHazardTitleKeyword in theKeywords:
        # We use safe translation infrastructure for this one (rather than Qt)
        myHazardTitle = safeTr(theKeywords[myHazardTitleKeyword])
    else:
        myHazardTitle = tr('Hazard layer')

    if myHazardSourceKeyword in theKeywords:
        # We use safe translation infrastructure for this one (rather than Qt)
        myHazardSource = safeTr(theKeywords[myHazardSourceKeyword])
    else:
        myHazardSource = tr('an unknown source')

    if myExposureTitleKeyword in theKeywords:
        myExposureTitle = theKeywords[myExposureTitleKeyword]
    else:
        myExposureTitle = tr('Exposure layer')

    if myExposureSourceKeyword in theKeywords:
        myExposureSource = theKeywords[myExposureSourceKeyword]
    else:
        myExposureSource = tr('an unknown source')

    myReport += ('<table class="table table-striped condensed'
                 ' bordered-table">')
    myReport += '<tr><th>%s</th></tr>' % myHazardDetails
    myReport += '<tr><td>%s%s %s.</td></tr>' % (
        myHazardTitle,
        myJoinWords,
        myHazardSource)

    myReport += '<tr><th>%s</th></tr>' % myExposureDetails
    myReport += '<tr><td>%s%s %s.</td></tr>' % (
        myExposureTitle,
        myJoinWords,
        myExposureSource)

    if theInaSAFEFlag:
        myReport += '<tr><th>%s</th></tr>' % tr('Software notes')
        myInaSAFEPhrase = tr(
            'This report was created using InaSAFE '
            'version %1. Visit http://inasafe.org to get '
            'your free copy of this software!').arg(get_version())
        myInaSAFEPhrase += tr(
            'InaSAFE has been jointly developed by'
            ' BNPB, AusAid & the World Bank')
        myReport += '<tr><td>%s</td></tr>' % myInaSAFEPhrase

    myReport += '</table>'

    return myReport
    
