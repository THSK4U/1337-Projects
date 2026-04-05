/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_itoa.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: tsellak <tsellak@student.1337.ma>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/26 17:07:11 by tsellak           #+#    #+#             */
/*   Updated: 2025/10/26 17:07:14 by tsellak          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

static int	l_int(long n)
{
	int	i;

	i = 0;
	if (n == 0)
		return (1);
	if (n < 0)
	{
		i++;
		n = -n;
	}
	while (n > 0)
	{
		n /= 10;
		i++;
	}
	return (i);
}

char	*ft_itoa(int n)
{
	char	*p;
	long	nbr;
	int		size;

	nbr = n;
	size = l_int(nbr);
	p = (char *)malloc((size + 1) * sizeof(char));
	if (!p)
		return (NULL);
	p[size] = '\0';
	if (nbr == 0)
		p[0] = '0';
	if (nbr < 0)
	{
		p[0] = '-';
		nbr = -nbr;
	}
	while (nbr > 0)
	{
		p[--size] = (nbr % 10) + '0';
		nbr /= 10;
	}
	return (p);
}
