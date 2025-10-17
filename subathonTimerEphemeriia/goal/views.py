from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404, render

from .models import Campaign
from .serializers import CampaignSerializer


@permission_required("subathonTimer.view_campaign")
def campaign_progress(request, campaign_id):
    campaign = get_object_or_404(Campaign, id=campaign_id, is_active=True)
    campaign_data = CampaignSerializer(campaign).data

    return render(
        request,
        "campaignProgress.html",
        {
            "campaign": campaign_data,
        },
    )
