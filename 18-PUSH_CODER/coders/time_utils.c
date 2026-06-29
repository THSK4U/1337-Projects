/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   time_utils.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: Tsellak <tsellak@student.1337.ma>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/29 08:58:53 by Tsellak           #+#    #+#             */
/*   Updated: 2026/06/29 08:58:53 by Tsellak          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

long	get_time_ms(void)
{
	struct timeval	tv;

	gettimeofday(&tv, NULL);
	return ((long)tv.tv_sec * 1000 + (long)(tv.tv_usec / 1000));
}

void	ms_to_timespec(struct timespec *ts, long ms)
{
	ts->tv_sec = ms / 1000;
	ts->tv_nsec = (ms % 1000) * 1000000;
}

long	get_next_timeout(t_coder *coder, t_dongle *dongle)
{
	long	now;
	long	timeout;

	now = get_time_ms();
	timeout = coder->deadline;
	if (!dongle->in_use && dongle->release_time > now
		&& dongle->release_time < timeout)
		timeout = dongle->release_time;
	return (timeout);
}

int	sleep_until_or_burnout(t_coder *coder, long duration_ms)
{
	long	end;
	long	now;

	end = get_time_ms() + duration_ms;
	while (1)
	{
		now = get_time_ms();
		if (now >= coder->deadline || simulation_check(coder->data))
			return (0);
		if (now >= end)
			return (1);
		if (end - now > 10)
			usleep(10000);
		else
			usleep(1000);
	}
}
